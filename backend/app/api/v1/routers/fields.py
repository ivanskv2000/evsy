from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import get_db

router = APIRouter(
    prefix="/fields",
    tags=["fields"]
)


@router.post("/", response_model=schemas.FieldOut, status_code=status.HTTP_201_CREATED)
def create_field(field: schemas.FieldCreate, db: Session = Depends(get_db)):
    db_field = crud.create_field(db=db, field=field)
    return db_field


@router.get("/", response_model=list[schemas.FieldOut])
def get_fields(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    fields = crud.get_fields(db=db, skip=skip, limit=limit)
    return fields


@router.get("/{field_id}", response_model=schemas.FieldOut)
def get_event(field_id: int, db: Session = Depends(get_db)):
    db_field = crud.get_field(db=db, field_id=field_id)
    if db_field is None:
        raise HTTPException(status_code=404, detail="Field not found")
    return db_field


@router.put("/{field_id}", response_model=schemas.FieldOut)
def update_field(field_id: int, field: schemas.FieldCreate, db: Session = Depends(get_db)):
    db_field = crud.update_field(db=db, field_id=field_id, field=field)
    if db_field is None:
        raise HTTPException(status_code=404, detail="Field not found")
    return db_field


@router.delete("/{field_id}", response_model=schemas.FieldOut)
def delete_field(field_id: int, db: Session = Depends(get_db)):
    db_field = crud.delete_field(db=db, field_id=field_id)
    if db_field is None:
        raise HTTPException(status_code=404, detail="Field not found")
    return db_field
