from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database.database import get_db

router = APIRouter(prefix="/fields", tags=["fields"])


@router.post(
    "/",
    response_model=schemas.FieldOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create a field",
    description="Create a new field that can be associated with events.",
    responses={
        201: {"description": "Field created successfully"},
    },
)
def create_field(field: schemas.FieldCreate, db: Session = Depends(get_db)):
    db_field = crud.create_field(db=db, field=field)
    return db_field


@router.get(
    "/",
    response_model=list[schemas.FieldOut],
    summary="List all fields",
    description="Return a paginated list of all fields that can be assigned to events.",
    responses={
        200: {"description": "List of fields returned"},
    },
)
def get_fields(db: Session = Depends(get_db)):
    fields = crud.get_fields(db=db)
    return fields


@router.get(
    "/{field_id}",
    response_model=schemas.FieldOut | schemas.FieldOutWithEventCount,
    summary="Get field by ID",
    description="Return a single field by its ID.",
    responses={
        200: {"description": "Field found"},
        404: {"description": "Field not found"},
    },
)
def get_field(
    field_id: int,
    with_event_count: bool = Query(False),
    db: Session = Depends(get_db),
):
    db_field = crud.get_field(db=db, field_id=field_id)
    if db_field is None:
        raise HTTPException(status_code=404, detail="Field not found")

    if with_event_count:
        count = crud.get_field_event_count(db=db, field_id=field_id)
        return schemas.FieldOutWithEventCount(**db_field.__dict__, event_count=count)

    return db_field


@router.put(
    "/{field_id}",
    response_model=schemas.FieldOut,
    summary="Update a field",
    description="Update the name, description, or type of a field.",
    responses={
        200: {"description": "Field updated"},
        404: {"description": "Field not found"},
    },
)
def update_field(
    field_id: int, field: schemas.FieldCreate, db: Session = Depends(get_db)
):
    db_field = crud.update_field(db=db, field_id=field_id, field=field)
    if db_field is None:
        raise HTTPException(status_code=404, detail="Field not found")
    return db_field


@router.delete(
    "/{field_id}",
    response_model=schemas.FieldOut,
    summary="Delete a field",
    description="Delete a field by its ID. This will remove the field from all related events.",
    responses={
        200: {"description": "Field deleted"},
        404: {"description": "Field not found"},
    },
)
def delete_field(field_id: int, db: Session = Depends(get_db)):
    db_field = crud.delete_field(db=db, field_id=field_id)
    if db_field is None:
        raise HTTPException(status_code=404, detail="Field not found")
    return db_field
