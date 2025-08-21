from fastapi import APIRouter, Depends, Response

from app.api.deps import get_settings
from app.modules.events.schemas import LinkType
from app.modules.fields.schemas import FieldType
from app.settings import Settings

router = APIRouter()


@router.get(
    "/ping",
    summary="Health check",
    description="Simple health check endpoint to verify API is running.",
    responses={200: {"description": "API is healthy"}},
)
def ping(settings: Settings = Depends(get_settings)):
    return {"pong": True, "debug_mode": settings.is_dev}


@router.get(
    "/config",
    summary="Get configuration",
    description="Get basic configuration information about the API instance.",
    responses={200: {"description": "Configuration returned"}},
)
def get_config(settings: Settings = Depends(get_settings)):
    return {
        "database_url": settings.database_url,
        "debug": settings.is_dev,
    }


@router.get(
    "/link-types",
    response_model=list[str],
    summary="Get link types",
    description="Get available link types for event external links (figma, confluence, etc).",
    responses={200: {"description": "List of available link types"}},
)
async def get_link_types(response: Response):
    response.headers["Cache-Control"] = "public, max-age=3600"
    return [link_type.value for link_type in LinkType]


@router.get(
    "/field-types",
    response_model=list[str],
    summary="Get field types",
    description="Get available field data types (string, number, boolean, etc).",
    responses={200: {"description": "List of available field types"}},
)
async def get_field_types(response: Response):
    response.headers["Cache-Control"] = "public, max-age=3600"
    return [field_type.value for field_type in FieldType]
