from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import get_db

router = APIRouter(
    prefix="/tags",
    tags=["tags"]
)


@router.post("/", response_model=schemas.TagOut, status_code=status.HTTP_201_CREATED)
def create_tag(tag: schemas.TagCreate, db: Session = Depends(get_db)):
    db_tag = crud.create_tag(db=db, tag=tag)
    return db_tag


@router.get("/", response_model=list[schemas.TagOut])
def get_tags(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tags = crud.get_tags(db=db, skip=skip, limit=limit)
    return tags


@router.get("/{tag_id}", response_model=schemas.TagOut)
def get_event(tag_id: str, db: Session = Depends(get_db)):
    db_tag = crud.get_tag(db=db, tag_id=tag_id)
    if db_tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    return db_tag


@router.put("/{tag_id}", response_model=schemas.TagOut)
def update_tag(tag_id: str, tag: schemas.TagCreate, db: Session = Depends(get_db)):
    db_tag = crud.update_tag(db=db, tag_id=tag_id, tag=tag)
    if db_tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    return db_tag


@router.delete("/{tag_id}", response_model=schemas.TagOut)
def delete_tag(tag_id: str, db: Session = Depends(get_db)):
    db_tag = crud.delete_tag(db=db, tag_id=tag_id)
    if db_tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    return db_tag