from pwdlib import PasswordHash
from app.core.config import settings 
from datetime import datetime,timedelta
from jose import jwt

password_hash = PasswordHash.recommended()  #create one hashing engine when the application starts


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return password_hash.verify(password, hashed_password)

def create_access_token(data: dict):
    to_encode=data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode["exp"] = expire
    encoded_jwt=jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
)
    return encoded_jwt

