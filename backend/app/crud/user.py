from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate

#To create a user we need a Database session,UserCreate,hashedpassword
def create_user(
    db:Session,
    user:UserCreate,  #with this UserCreate we can access user.username,user.email,user.password
    hashed_password:str):

    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )

    db.add(new_user) #adds object to the SQLAlchemy session
    db.commit()  #saves transaction to PostgreSQL
    db.refresh(new_user)  #reloads the python object with updated database values
    return new_user

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()