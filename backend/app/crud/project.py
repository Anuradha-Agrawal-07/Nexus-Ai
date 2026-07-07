from sqlalchemy.orm import Session
from uuid import UUID
from app.models.project import Project
from app.models.user import User

from app.schemas.project import (
    ProjectCreate,
    ProjectResponse,
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

def get_projects_by_owner(
    db: Session,
    owner_id: UUID
):
    return db.query(Project).filter(Project.owner_id==owner_id).all()

def get_project_by_id(
    db: Session,
    project_id:UUID,
    owner_id:UUID
):
    return db.query(Project).filter(Project.id==project_id,Project.owner_id==owner_id).first()

def update_project(
    db: Session ,
    project: Project,
    project_update:ProjectUpdate
):
    update_data = project_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(project, key, value)
        #If user sends  
        # {
        #     "name": "Nexus AI v2"
        # }
        #setattr makes it equivalent to project.name="Nexus AI v2"
    db.commit()
    db.refresh(project)
    return project

def delete_project(
    db:Session,
    project:Project
):
    db.delete(project)
    db.commit()
    return 