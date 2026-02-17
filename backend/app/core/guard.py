from fastapi import Depends, HTTPException, status

from app.settings import get_settings


def ensure_not_demo(settings=Depends(get_settings)):
    if settings.is_demo:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "code": "action_forbidden_in_demo",
                "message": "This action is not allowed in demo mode.",
            },
        )


def ensure_dev(settings=Depends(get_settings)):
    if not settings.is_dev:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "code": "action_requires_dev_mode",
                "message": "This action is allowed only in development.",
            },
        )
