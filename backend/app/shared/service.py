from app.modules.events.models import Event
from app.modules.fields.models import Field
from app.modules.tags.models import Tag
from sqlalchemy.orm import Session
from fastapi import HTTPException

def assert_db_empty(db: Session):
    if db.query(Event).first() or db.query(Field).first() or db.query(Tag).first():
        raise HTTPException(
            status_code=405, detail="Action is only allowed on empty database"
        )