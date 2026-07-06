from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.db.database import get_db

from app.schemas.user import UserCreate, UserResponse

from app.crud.user import (
    get_user_by_email,
    create_user
)

from app.schemas.auth import LoginRequest, Token

from app.services.security import (
    hash_password,
    verify_password,
    create_access_token,
)
router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)
@router.post(
    "/register",
    response_model=UserResponse,
    status_code=201  #client's request was successfully fulfilled
)
def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    existing_user = get_user_by_email(db, user.email)

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="User already exists"
        )

    hashed_password = hash_password(user.password)

    new_user = create_user(
        db,
        user,
        hashed_password
    )

    return new_user

    
@router.post(
    "/login",
    response_model=Token,
    status_code=201
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    existing_user = get_user_by_email(db, form_data.username)

    if not existing_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(
        form_data.password,
        existing_user.hashed_password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    data = {
        "sub": str(existing_user.id),
        "role": existing_user.role
    }

    token = create_access_token(data)

    return {
        "access_token": token,
        "token_type": "bearer"
    }
