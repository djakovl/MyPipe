from passlib.context import CryptContext
import uuid
import random
import string
from datetime import datetime, timedelta
from typing import Optional

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def generate_uuid() -> str:
    return str(uuid.uuid4())


def generate_user_link() -> str:
    random_part = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    return random_part


def generate_timestamp() -> str:
    return datetime.utcnow().isoformat() + "Z"


def is_valid_email(email: str) -> bool:
    return "@" in email and "." in email.split("@")[1]
