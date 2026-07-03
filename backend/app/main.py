from fastapi import FastAPI
from app.core.config import settings
from app.db.database import engine


app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION
)

@app.get("/")
async def root():
    return {

        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running"
    }