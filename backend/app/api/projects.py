from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)
from uuid import UUID
from sqlalchemy.orm import Session

from app.db.database import get_db

from app.schemas.project import (
    ProjectCreate,
    ProjectResponse,
    ProjectUpdate
)

from app.crud.project import (
    get_project_by_name,
    create_project,
    get_projects_by_owner,
    get_project_by_id,
    update_project,
    delete_project
)

from app.models.user import User

from app.services.security import get_current_user

router = APIRouter(
    prefix="/projects",
    tags=["Projects"]
)

@router.post(
    "/",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED
)
def create_new_project(
    project: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    existing_project=get_project_by_name(db,current_user.id,project.name)
    if existing_project:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Project already exists"
        )
    new_project=create_project(db,project,current_user)
    return new_project

@router.get(
    "/",
    response_model=list[ProjectResponse]
)
def get_my_projects(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    projects=get_projects_by_owner(db,current_user.id)
    return projects

@router.get(
    "/{project_id}",
    response_model=ProjectResponse
)
def get_project(
    project_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    project=get_project_by_id(db,project_id,current_user.id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project doesn't exist"
        )
    return project

@router.patch(
    "/{project_id}",
    response_model=ProjectUpdate
)
def update_existing_project(
    project_id:UUID,
    project_update:ProjectUpdate,
    db:Session=Depends(get_db), 
    current_user:User=Depends(get_current_user)

):
    project=get_project_by_id(db,project_id,current_user.id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project doesn't exist"
        )
    updated_project=update_project(db,project,project_update)
    return updated_project

@router.delete(
    "/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_existing_project(
    project_id:UUID,
    db:Session=Depends(get_db), 
    current_user:User=Depends(get_current_user)
):
    project=get_project_by_id(db,project_id,current_user.id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project doesn't exist"
        )
    delete_project(db,project)
    return