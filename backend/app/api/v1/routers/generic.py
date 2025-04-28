from fastapi import APIRouter, Response, Depends
from app.deps import get_settings
from app.settings import Settings
from app.schemas import LinkType, FieldType

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

@router.get("/link-types", response_model=list[str])
async def get_link_types(response: Response):
    response.headers["Cache-Control"] = "public, max-age=3600"
    return [link_type.value for link_type in LinkType]

@router.get("/field-types", response_model=list[str])
async def get_field_types(response: Response):
    response.headers["Cache-Control"] = "public, max-age=3600"
    return [field_type.value for field_type in FieldType]
