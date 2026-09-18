"""
Outlook360 - Database Configuration
Supports dual engine modes: MySQL 8.0+ (Production) and SQLite (Presentation mode).
"""
import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


class DatabaseConfig:
    """Database connection and pooling configurations."""
    ENGINE_TYPE: str = os.getenv("DB_ENGINE", "sqlite").lower()

    # MySQL Parameters
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: int = int(os.getenv("DB_PORT", 3306))
    DB_USER: str = os.getenv("DB_USER", "root")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "root")
    DB_NAME: str = os.getenv("DB_NAME", "outlook360_bi")

    # SQLite Parameters
    SQLITE_PATH: str = os.getenv("SQLITE_DB_PATH", "database/outlook360.db")

    @classmethod
    def get_sqlite_absolute_path(cls) -> Path:
        """Returns the absolute path to the SQLite database file."""
        return BASE_DIR / cls.SQLITE_PATH

    @classmethod
    def get_sqlalchemy_url(cls, force_sqlite: bool = False) -> str:
        """
        Constructs the SQLAlchemy connection URI.
        If force_sqlite is True or ENGINE_TYPE is sqlite, returns SQLite URL.
        Otherwise returns MySQL URL.
        """
        if force_sqlite or cls.ENGINE_TYPE == "sqlite":
            sqlite_file = cls.get_sqlite_absolute_path()
            sqlite_file.parent.mkdir(parents=True, exist_ok=True)
            # Use forward slashes for SQLite URI on Windows
            return f"sqlite:///{sqlite_file.as_posix()}"
        
        # MySQL Connection URL via mysqlconnector
        return (
            f"mysql+mysqlconnector://{cls.DB_USER}:{cls.DB_PASSWORD}"
            f"@{cls.DB_HOST}:{cls.DB_PORT}/{cls.DB_NAME}"
        )

    @classmethod
    def get_mysql_raw_params(cls) -> dict:
        """Returns dictionary of connection parameters for mysql.connector."""
        return {
            "host": cls.DB_HOST,
            "port": cls.DB_PORT,
            "user": cls.DB_USER,
            "password": cls.DB_PASSWORD,
            "database": cls.DB_NAME
        }
