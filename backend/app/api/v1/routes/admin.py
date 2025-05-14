from fastapi import APIRouter

from app.modules.admin.io.router import router as io_router
from app.modules.admin.seed.router import router as seed_router

router = APIRouter(prefix="/admin")
router.include_router(io_router)
router.include_router(seed_router)
