"""
Ensure Store Owner demo account is seeded and test authentication.
"""
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from database.seed_data import seed_default_users
from database.auth import auth_manager

if __name__ == "__main__":
    print("Seeding default users...")
    seed_default_users()
    
    print("\nTesting authentication for Store Owner demo login (smt10@gmail.com / 12345)...")
    user = auth_manager.authenticate_user("smt10@gmail.com", "12345")
    if user:
        print(f"  [SUCCESS] Authenticated User: {user['full_name']} | Role: {user['role']} | Email: {user['email']}")
    else:
        print("  [ERROR] Authentication failed for smt10@gmail.com / 12345")
        sys.exit(1)
