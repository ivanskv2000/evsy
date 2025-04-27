from fastapi import APIRouter, Depends
from app.deps import get_settings
from app.settings import Settings

router = APIRouter()

@router.get("/ping")
def ping(settings: Settings = Depends(get_settings)):
    return {"pong": True, "debug_mode": settings.debug}


@router.get("/config")
def get_config(settings: Settings = Depends(get_settings)):
    return {
        "database_url": settings.database_url,
        "debug": settings.debug,
    }
