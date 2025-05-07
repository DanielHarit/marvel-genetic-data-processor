import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.user import User
from app.core.security import get_password_hash

def create_test_users(db: Session) -> None:
    # Create admin user
    admin = User(
        email="admin@example.com",
        username="admin",
        hashed_password=get_password_hash("admin123"),
        is_superuser=True,
        is_active=True
    )
    db.add(admin)

    # Create regular user
    user = User(
        email="user@example.com",
        username="user",
        hashed_password=get_password_hash("user123"),
        is_superuser=False,
        is_active=True
    )
    db.add(user)

    # Create inactive user
    inactive_user = User(
        email="inactive@example.com",
        username="inactive",
        hashed_password=get_password_hash("inactive123"),
        is_superuser=False,
        is_active=False
    )
    db.add(inactive_user)

    db.commit()
    print("Test users created successfully!")

if __name__ == "__main__":
    db = SessionLocal()
    try:
        create_test_users(db)
        users = db.query(User).all()
        for user in users:
            print(user.username)
            print(user.email)
            print(user.is_superuser)
            print(user.is_active)
            print(user.hashed_password)
            print("--------------------------------")
    finally:
        db.close() 