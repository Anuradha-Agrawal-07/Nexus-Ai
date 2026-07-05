from pydantic import BaseModel,EmailStr
from uuid import UUID

class UserCreate(BaseModel): #What information does a client need to create a user
    username:str
    email:EmailStr
    password:str

class UserResponse(BaseModel): #What information does a server need to send back?
    id:UUID
    username:str
    email:EmailStr
    class Config: #with this we tell pydantic that this object isn't a dictionary. Read its attributes.
        from_attributes = True