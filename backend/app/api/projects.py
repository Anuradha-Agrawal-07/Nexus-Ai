from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)

from sqlalchemy.orm import Session

from app.db.database import get_db

from app.schemas.project import (
    ProjectCreate,
    ProjectResponse,
    ProjectUpdate
)

from app.crud.project import (
    get_project_by_name,
    create_project
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