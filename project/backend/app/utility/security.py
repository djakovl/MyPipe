from passlib.context import CryptContext
import uuid
import random
import string
from datetime import datetime

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def generate_uuid() -> str:
    return str(uuid.uuid4())


def generate_user_link() -> str:
    random_part = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    return random_part


def generate_timestamp() -> str:
    return datetime.utcnow().isoformat() + "Z"
