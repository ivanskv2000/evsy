from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db

from .service import seed_all

router = APIRouter(prefix="/seed", tags=["seed"])


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Seed the database with example data",
    description="Run module-specific seeding functions to populate the database with test/demo data.",
    responses={
        201: {"description": "Seeding completed successfully"},
    },
)
def seed_data(db: Session = Depends(get_db)):
    seed_all(db)
    return {"status": "ok"}
