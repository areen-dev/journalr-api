import os
from datetime import datetime, timedelta

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWSError, jwt
from passlib.context import CryptContext

from database import get_db
from models import User
from schemas import UserCreate, UserResponse

router = APIRouter()
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY", "fallback-key")
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_token(data: dict) -> str:
    expiry_time = datetime.now() + timedelta(hours=24)
    data["exp"] = expiry_time
    token = jwt.encode(data, SECRET_KEY, ALGORITHM)
    return token


@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db=Depends(get_db)):
    db_entry = db.query(User).filter(User.username == user.username).first()
    if db_entry is not None:
        raise HTTPException(status_code=409, detail="Username already exists")
    hash_pass = hash_password(user.password)
    new_user = User(username=user.username, hashed_password=hash_pass)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login")
def login(user: UserCreate, db=Depends(get_db)):
    db_entry = db.query(User).filter(User.username == user.username).first()
    if db_entry is None:
        raise HTTPException(status_code=404, detail="Username not found")
    user_pass = verify_password(user.password, db_entry.hashed_password)
    if user_pass is not True:
        raise HTTPException(status_code=401, detail="password does not match")
    return create_token({"username": db_entry.username})


@router.get("/protected")
def protected_route(token: str = Depends(oauth2_scheme)):
    try:
        jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWSError:
        raise HTTPException(status_code=498, detail="invalid jwt token")
    return {"message": "Access granted"}
