from sqlalchemy.orm import Session
from uuid import UUID
from app.models.project import Project
from app.models.api_key import APIKey

from app.schemas.api_key import (
    APIKeyCreate,
    APIKeyResponse,
    APIKeyUpdate
)
from app.services.encryption import encrypt_api_key

def get_api_key_by_provider(
    db:Session,
    project_id:UUID,
    provider:str
):
    return db.query(APIKey).filter(APIKey.project_id==project_id,APIKey.provider==provider).first()

def create_api_key(
    db: Session,
    api_key: APIKeyCreate,
    project: Project
):
    encrypted_key = encrypt_api_key(api_key.api_key)
    new_api_key = APIKey(
    provider=api_key.provider,
    encrypted_key=encrypted_key,
    project_id=project.id
)
    db.add(new_api_key)
    db.commit()
    db.refresh(new_api_key)
    return new_api_key
    

def get_api_keys_by_project(
    db: Session,
    project_id: UUID
):
    return db.query(APIKey).filter(APIKey.project_id==project_id).all()

def get_api_key_by_id(
    db: Session,
    key_id: UUID
):
    return db.query(APIKey).filter(APIKey.id==key_id).first()

def update_api_key(
    db: Session,
    api_key: APIKey,
    api_key_update: APIKeyUpdate
):
    if api_key_update.api_key is not None:
        encrypted_api_key=encrypt_api_key(api_key_update.api_key)
        api_key.encrypted_key=encrypted_api_key
    db.commit()
    db.refresh(api_key)
    return api_key


def delete_api_key(
    db: Session,
    api_key: APIKey
):
    db.delete(api_key)
    db.commit()
    return 