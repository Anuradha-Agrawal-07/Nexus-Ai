from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class ProjectCreate(BaseModel):
    name: str
    description: str | None = None


class ProjectResponse(ProjectCreate): #What information does a server need to send back?
    id:UUID
    owner_id:UUID
    created_at:datetime
    updated_at:datetime
    class Config: #with this we tell pydantic that this object isn't a dictionary. Read its attributes.
        from_attributes = True

class ProjectUpdate(BaseModel):
    name: str | None = None
    description: str | None = None