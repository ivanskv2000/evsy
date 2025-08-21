from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.auth.token import get_current_user
from app.modules.fields import crud as field_crud
from app.modules.fields.schemas import FieldCreate, FieldOut, FieldOutWithEventCount

router = APIRouter(
    prefix="/fields", tags=["fields"], dependencies=[Depends(get_current_user)]
)


@router.post(
    "/",
    response_model=FieldOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create a field",
    description="Create a new field that can be associated with events.",
    responses={
        201: {"description": "Field created successfully"},
        400: {"description": "Validation error"}
    }
)
def create_field_route(field: FieldCreate, db: Session = Depends(get_db)):
    return field_crud.create_field(db=db, field=field)


@router.get(
    "/",
    response_model=list[FieldOut],
    summary="List all fields",
    description="Return a paginated list of all fields that can be assigned to events.",
    responses={
        200: {"description": "List of fields returned successfully"}
    }
)
def list_fields_route(db: Session = Depends(get_db)):
    return field_crud.get_fields(db=db)


@router.get(
    "/{field_id}",
    response_model=FieldOut | FieldOutWithEventCount,
    summary="Get field by ID",
    description="Return a single field by its ID. Optionally include count of events using this field.",
    responses={
        200: {"description": "Field found and returned"},
        404: {"description": "Field not found"}
    }
)
def get_field_route(
    field_id: int,
    with_event_count: bool = Query(False, description="Include count of events using this field"),
    db: Session = Depends(get_db),
):
    db_field = field_crud.get_field(db=db, field_id=field_id)
    if db_field is None:
        raise HTTPException(status_code=404, detail="Field not found")

    if with_event_count:
        count = field_crud.get_field_event_count(db=db, field_id=field_id)
        return FieldOutWithEventCount(**db_field.__dict__, event_count=count)

    return db_field


@router.put(
    "/{field_id}",
    response_model=FieldOut,
    summary="Update a field",
    description="Update the name, description, or type of a field.",
    responses={
        200: {"description": "Field updated successfully"},
        404: {"description": "Field not found"},
        400: {"description": "Validation error"}
    }
)
def update_field_route(
    field_id: int, field: FieldCreate, db: Session = Depends(get_db)
):
    db_field = field_crud.update_field(db=db, field_id=field_id, field=field)
    if db_field is None:
        raise HTTPException(status_code=404, detail="Field not found")
    return db_field


@router.delete(
    "/{field_id}",
    response_model=FieldOut,
    summary="Delete a field",
    description="Delete a field by its ID. This will remove the field from all related events.",
    responses={
        200: {"description": "Field deleted successfully"},
        404: {"description": "Field not found"}
    }
)
def delete_field_route(field_id: int, db: Session = Depends(get_db)):
    db_field = field_crud.delete_field(db=db, field_id=field_id)
    if db_field is None:
        raise HTTPException(status_code=404, detail="Field not found")
    return db_field
