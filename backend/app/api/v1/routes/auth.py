from fastapi import APIRouter

from app.modules.auth.router import router as auth_router

router = APIRouter(prefix="/auth", tags=["auth"])

router.include_router(auth_router)
