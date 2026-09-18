"""
OmniPulse AI - Universal Database Connection & Engine Manager
Provides thread-safe connection pooling, automatic schema initialization,
and seamless dual-engine support for both MySQL and SQLite.
"""
import os
import sys
from pathlib import Path
from typing import Optional, Any, Dict, List
import pandas as pd
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.engine import Engine

# Ensure project root in sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from config.database_config import DatabaseConfig
from config.settings import AppSettings


class DatabaseManager:
    """Manages database connectivity, schema bootstrapping, and SQL query execution."""

    _instance: Optional['DatabaseManager'] = None
    _engine: Optional[Engine] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            cls._instance._initialize_engine()
        return cls._instance

    def _initialize_engine(self) -> None:
        """Initializes the SQLAlchemy engine with connection pooling."""
        try:
            # First attempt connection based on configured engine type
            if DatabaseConfig.ENGINE_TYPE == "mysql":
                try:
                    import mysql.connector
                    # Test MySQL connection first
                    conn_params = DatabaseConfig.get_mysql_raw_params()
                    # Connect without database first to ensure DB exists
                    temp_conn = mysql.connector.connect(
                        host=conn_params["host"],
                        port=conn_params["port"],
                        user=conn_params["user"],
                        password=conn_params["password"]
                    )
                    cursor = temp_conn.cursor()
                    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {conn_params['database']}")
                    cursor.close()
                    temp_conn.close()

                    url = DatabaseConfig.get_sqlalchemy_url(force_sqlite=False)
                    self._engine = create_engine(url, pool_recycle=3600, pool_pre_ping=True)
                    # Verify connectivity
                    with self._engine.connect() as conn:
                        conn.execute(text("SELECT 1"))
                    print("[Outlook360 DB] Successfully connected to MySQL server.")
                except Exception as e:
                    print(f"[Outlook360 DB] MySQL connection failed ({e}). Falling back to portable SQLite engine.")
                    url = DatabaseConfig.get_sqlalchemy_url(force_sqlite=True)
                    self._engine = create_engine(url, connect_args={"check_same_thread": False})
            else:
                url = DatabaseConfig.get_sqlalchemy_url(force_sqlite=True)
                self._engine = create_engine(url, connect_args={"check_same_thread": False})
                print("[Outlook360 DB] Initialized SQLite Database Engine.")

        except Exception as e:
            print(f"[Outlook360 DB Error] Could not initialize database engine: {e}")
            # Final fallback to local sqlite
            sqlite_path = DatabaseConfig.get_sqlite_absolute_path()
            sqlite_path.parent.mkdir(parents=True, exist_ok=True)
            self._engine = create_engine(f"sqlite:///{sqlite_path.as_posix()}", connect_args={"check_same_thread": False})

        self.ensure_schema()

    @property
    def engine(self) -> Engine:
        """Returns the active SQLAlchemy Engine instance."""
        if self._engine is None:
            self._initialize_engine()
        return self._engine

    def is_sqlite(self) -> bool:
        """Checks if current engine is SQLite."""
        return "sqlite" in str(self.engine.url)

    def ensure_schema(self) -> None:
        """Reads schema.sql and creates tables if they do not exist."""
        schema_path = AppSettings.DATABASE_DIR / "schema.sql"
        if not schema_path.exists():
            return

        with open(schema_path, "r", encoding="utf-8") as f:
            raw_sql = f.read()

        # Adjust for MySQL if connected to MySQL
        if not self.is_sqlite():
            raw_sql = raw_sql.replace("INTEGER PRIMARY KEY AUTOINCREMENT", "INT AUTO_INCREMENT PRIMARY KEY")
            raw_sql = raw_sql.replace("INTEGER", "INT")

        # Split and execute statements
        statements = [stmt.strip() for stmt in raw_sql.split(";") if stmt.strip()]

        with self.engine.begin() as conn:
            for stmt in statements:
                # SQLite doesn't support ON DELETE RESTRICT in some setups, but handles it cleanly
                try:
                    conn.execute(text(stmt))
                except Exception as ex:
                    # Ignore harmless index or duplicate table warnings
                    pass

    def execute_query(self, query_str: str, params: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
        """
        Executes a SQL SELECT query and returns the result as a pandas DataFrame.
        """
        with self.engine.connect() as conn:
            return pd.read_sql(text(query_str), conn, params=params)

    def execute_non_query(self, sql_str: str, params: Optional[Dict[str, Any]] = None) -> int:
        """
        Executes an INSERT, UPDATE, or DELETE query and returns row count.
        """
        with self.engine.begin() as conn:
            result = conn.execute(text(sql_str), params or {})
            return result.rowcount

    def get_table_names(self) -> List[str]:
        """Returns a list of all tables present in the database."""
        inspector = inspect(self.engine)
        return inspector.get_table_names()

    def get_row_count(self, table_name: str) -> int:
        """Returns the total number of rows in a given table."""
        try:
            df = self.execute_query(f"SELECT COUNT(*) AS cnt FROM {table_name}")
            return int(df["cnt"].iloc[0]) if not df.empty else 0
        except Exception:
            return 0


# Singleton global accessor
db_manager = DatabaseManager()
