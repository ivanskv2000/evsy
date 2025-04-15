from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import crud, schemas, models
from app.database import get_db

router = APIRouter(
    prefix="/events",
    tags=["events"]
)


@router.post("/", response_model=schemas.EventOut, status_code=status.HTTP_201_CREATED)
def create_event(event: schemas.EventCreate, db: Session = Depends(get_db)):
    db_fields = crud.get_fields_by_ids(db, event.fields)
    db_tags = crud.get_or_create_tags(db, event.tags)

    if len(db_fields) != len(event.fields):
        raise HTTPException(status_code=400, detail="One or more fields do not exist.")
    
    db_event = crud.create_event(db=db, event=event)
    return db_event


@router.get("/{event_id}", response_model=schemas.EventOut)
def get_event(event_id: int, db: Session = Depends(get_db)):
    db_event = crud.get_event(db=db, event_id=event_id)
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return db_event


@router.get("/", response_model=list[schemas.EventOut])
def get_events(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    events = crud.get_events(db=db, skip=skip, limit=limit)
    return events


@router.put("/{event_id}", response_model=schemas.EventOut)
def update_event(event_id: int, event: schemas.EventCreate, db: Session = Depends(get_db)):
    db_fields = crud.get_fields_by_ids(db, event.fields)

    if len(db_fields) != len(event.fields):
        raise HTTPException(status_code=400, detail="One or more fields do not exist.")
    
    db_event = crud.update_event(db=db, event_id=event_id, event=event)
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return db_event


@router.delete("/{event_id}", response_model=schemas.EventOut)
def delete_event(event_id: int, db: Session = Depends(get_db)):
    db_event = crud.delete_event(db=db, event_id=event_id)
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return db_event
