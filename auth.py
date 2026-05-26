from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta

pwd_context = CryptContext(schemes=["bcrypt"])


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


SECRET_KEY = "fmttm"
ALGORITHM = "HS256"


def create_token(data: dict) -> str:
    expiry_time = datetime.now() + timedelta(hours=24)
    data["exp"] = expiry_time
    token = jwt.encode(data, SECRET_KEY, ALGORITHM)
    return token
