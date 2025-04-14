from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import get_db

router = APIRouter(
    prefix="/fields",
    tags=["fields"]
)


@router.post("/", response_model=schemas.Field)
def create_field(field: schemas.FieldCreate, db: Session = Depends(get_db)):
    db_field = crud.create_field(db=db, field=field)
    return db_field


@router.get("/", response_model=list[schemas.Field])
def get_fields(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    fields = crud.get_fields(db=db, skip=skip, limit=limit)
    return fields
