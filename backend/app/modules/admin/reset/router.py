from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db

from .service import count_entities, reset_database

router = APIRouter(prefix="/reset", tags=["reset"])


@router.post(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Reset all data",
    description=(
        "Delete all tags, fields, and events. Use with caution. "
        "Set `dry_run=true` to simulate the reset without deleting anything."
    ),
    responses={
        200: {"description": "Reset performed or dry-run preview returned"},
    },
)
def reset_all_data(
    dry_run: bool = Query(
        True, description="If true, return number of records that would be deleted."
    ),
    db: Session = Depends(get_db),
):
    if dry_run:
        return {"would_delete": count_entities(db)}

    reset_database(db)
    return {"status": "ok"}
