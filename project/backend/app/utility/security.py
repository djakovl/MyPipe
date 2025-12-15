"""
Security utilities for password hashing and JWT
"""
from passlib.context import CryptContext
import uuid
import random
import string
from datetime import datetime, timedelta
from typing import Optional

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash"""
    return pwd_context.verify(plain_password, hashed_password)


def generate_uuid() -> str:
    """Generate a UUID"""
    return str(uuid.uuid4())


def generate_user_link() -> str:
    """Generate a random user link (e.g., 'username-abc123')"""
    random_part = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    return random_part


def generate_timestamp() -> str:
    """Generate current timestamp in ISO format"""
    return datetime.utcnow().isoformat() + "Z"


def is_valid_email(email: str) -> bool:
    """Basic email validation"""
    return "@" in email and "." in email.split("@")[1]
