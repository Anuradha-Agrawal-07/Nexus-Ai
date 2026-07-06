from fastapi import FastAPI
from app.core.config import settings
from app.db.database import engine


app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION
)

from app.api.auth import router as auth_router
from app.api.users import router as users_router
app.include_router(auth_router)
app.include_router(users_router)
@app.get("/")
async def root():
    return {

        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running"
    }