from fastapi import Depends, HTTPException

from app.settings import get_settings


def ensure_not_demo(settings=Depends(get_settings)):
    if settings.is_demo:
        raise HTTPException(
            status_code=403, detail="This action is not allowed in demo mode."
        )


def ensure_dev(settings=Depends(get_settings)):
    if not settings.is_dev:
        raise HTTPException(
            status_code=403, detail="This action is allowed only in development."
        )
