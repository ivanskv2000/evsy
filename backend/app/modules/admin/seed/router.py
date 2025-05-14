from fastapi import APIRouter

router = APIRouter(prefix="/seed", tags=["Admin seeding"])


@router.post("/seed")
def seed_database():
    pass
