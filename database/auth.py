"""
Outlook360 - Authentication & Role-Based Access Control (RBAC) Module
Provides password hashing, credential validation, and user session management.
"""
import sys
import hashlib
from pathlib import Path
from typing import Optional, Dict, Any, List
import pandas as pd
from sqlalchemy import text

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from database.connection import db_manager


class AuthManager:
    """Manages user authentication and role verification."""

    @staticmethod
    def hash_password(password: str) -> str:
        """Generates SHA-256 hash for password storage."""
        salt = "outlook360_enterprise_salt_2026"
        return hashlib.sha256((password + salt).encode('utf-8')).hexdigest()

    @classmethod
    def authenticate_user(cls, identifier: str, password: str) -> Optional[Dict[str, Any]]:
        """
        Validates credentials by Email (Store Owner) or Employee ID (Cashier / Inventory Staff).
        Returns user dictionary if authenticated, otherwise None.
        """
        clean_id = identifier.strip().lower()
        pwd_hash = cls.hash_password(password.strip())

        query = """
        SELECT user_id, emp_id, email, full_name, role, is_active
        FROM users
        WHERE (LOWER(email) = :id OR LOWER(emp_id) = :id)
          AND password_hash = :hash
          AND is_active = 1
        LIMIT 1;
        """
        df = db_manager.execute_query(query, params={"id": clean_id, "hash": pwd_hash})
        if not df.empty:
            return df.iloc[0].to_dict()
        return None

    @classmethod
    def create_user(
        cls,
        emp_id: str,
        email: str,
        password: str,
        full_name: str,
        role: str
    ) -> bool:
        """Registers a new employee or staff user."""
        pwd_hash = cls.hash_password(password)
        sql = """
        INSERT INTO users (emp_id, email, password_hash, full_name, role, is_active)
        VALUES (:emp, :email, :hash, :name, :role, 1)
        """
        try:
            db_manager.execute_non_query(sql, {
                "emp": emp_id.strip().upper(),
                "email": email.strip().lower(),
                "hash": pwd_hash,
                "name": full_name.strip(),
                "role": role.strip().lower()
            })
            return True
        except Exception as e:
            print(f"[Auth Error] User creation failed: {e}")
            return False

    @staticmethod
    def get_all_users() -> pd.DataFrame:
        """Fetches all system users for Owner admin management."""
        query = "SELECT user_id, emp_id, email, full_name, role, is_active, created_at FROM users ORDER BY user_id ASC"
        return db_manager.execute_query(query)


auth_manager = AuthManager()
