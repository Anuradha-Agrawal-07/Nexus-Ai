from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)

from uuid import UUID

from sqlalchemy.orm import Session

from app.db.database import get_db

from app.schemas.api_key import (
    APIKeyCreate,
    APIKeyResponse,
    APIKeyUpdate
)

from app.crud.api_key import (
    get_api_key_by_provider,
    create_api_key,
    get_api_keys_by_project,
    get_api_key_by_id,
    update_api_key,
    delete_api_key
)

from app.crud.project import (
    get_project_by_id
)

from app.models.user import User

from app.services.security import get_current_user

router = APIRouter(
    prefix="/projects",
    tags=["API Keys"]
)
@router.post(
    "/{project_id}/keys",
    response_model=APIKeyResponse,
    status_code=status.HTTP_201_CREATED
)
def create_new_api_key(
    project_id: UUID,
    api_key: APIKeyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    project=get_project_by_id(db,project_id,current_user.id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No such project exist"   
        )
    existing_api_key = get_api_key_by_provider(db,project.id,api_key.provider)
    if existing_api_key:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="API key for this provider already exists."
    )
    new_api_key=create_api_key(db,api_key,project)
    return new_api_key


@router.get(
    "/{project_id}/keys",
    response_model=list[APIKeyResponse]
)
def get_api_keys(
    project_id:UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    project=get_project_by_id(db,project_id,current_user.id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No such project exist"   
        )
    api_keys=get_api_keys_by_project(db,project.id)
    return api_keys

@router.patch(
    "/keys/{key_id}",
    response_model=APIKeyResponse
)

# Get API key by ID

# ↓

# 404 if not found

# ↓

# Does it belong to the current user?

# ↓

# 403 Forbidden (or 404 if you prefer not to reveal existence)

# ↓

# Update the API key
# (encrypt inside CRUD)

# ↓

# Return APIKeyResponse
def update_existing_api_key(
    key_id: UUID,
    api_key_update: APIKeyUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    
    api_key = get_api_key_by_id(db,key_id)
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="API key not found"
        )
    if api_key.project.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this API key"
    )
    updated_api_key=update_api_key(db,api_key,api_key_update)
    return updated_api_key

@router.delete(
    "/keys/{key_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_existing_api_key(
    key_id:UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    api_key = get_api_key_by_id(db,key_id)
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="API key not found"
        )
    if api_key.project.owner_id != current_user.id:
        raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Not authorized to access this API key"
    )
    delete_api_key(db, api_key)
    return 