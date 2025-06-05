from fastapi import APIRouter, Depends

from app.modules.admin.io.router import router as io_router
from app.modules.admin.reset.router import router as reset_router
from app.modules.admin.seed.router import router as seed_router
from app.modules.auth.token import get_current_user

router = APIRouter(prefix="/admin", dependencies=[Depends(get_current_user)])

router.include_router(io_router)
router.include_router(seed_router)
router.include_router(reset_router)
