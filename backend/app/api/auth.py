from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db

from app.schemas.user import UserCreate, UserResponse

from app.crud.user import (
    get_user_by_email,
    create_user
)

from app.services.security import hash_password

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