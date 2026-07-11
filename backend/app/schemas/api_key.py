from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class APIKeyCreate(BaseModel):
    provider: str
    api_key: str


class APIKeyResponse(BaseModel):
    id:UUID
    provider:str
    created_at:datetime
    updated_at:datetime
    class Config: #with this we tell pydantic that this object isn't a dictionary. Read its attributes.
        from_attributes = True
    
class APIKeyUpdate(BaseModel):
    api_key: str | None = None
