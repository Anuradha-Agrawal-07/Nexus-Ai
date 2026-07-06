from pwdlib import PasswordHash
from app.core.config import settings 
from datetime import datetime,timedelta,timezone

password_hash = PasswordHash.recommended()  #create one hashing engine when the application starts
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.crud.user import get_user_by_id
from app.core.config import settings

def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return password_hash.verify(password, hashed_password)

def create_access_token(data: dict):
    to_encode=data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode["exp"] = expire
    encoded_jwt=jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
)
    return encoded_jwt


def verify_token(token:str):
    try:
        payload=jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM
        )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="auth/login"
)

def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    try:
        payload = jwt.decode(
                        token,
                        settings.SECRET_KEY,
                        algorithms=[settings.ALGORITHM]
                    )
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials"
            )
        user=get_user_by_id(db,user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials"
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized"
        )
    return user

