from sqlalchemy.orm import Session
from uuid import UUID
from app.models.project import Project
from app.models.user import User

from app.schemas.project import (
    ProjectCreate,
    ProjectUpdate
)

def get_project_by_name(
    db: Session,
    owner_id: UUID,
    name: str
):
    return db.query(Project).filter(Project.name == name,Project.owner_id==owner_id).first()

def create_project(
    db: Session,
    project: ProjectCreate,
    current_user: User
):
    new_project=Project(name=project.name,
    description=project.description,
    owner_id=current_user.id)
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project