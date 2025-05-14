from sqlalchemy.orm import Session

from app.modules.events.models import Event
from app.modules.fields.models import Field
from app.modules.tags.models import Tag


def reset_database(db: Session):
    for model in [Event, Field, Tag]:
        for obj in db.query(model).all():
            db.delete(obj)
    db.commit()


def count_entities(db: Session) -> dict:
    return {
        "events": db.query(Event).count(),
        "fields": db.query(Field).count(),
        "tags": db.query(Tag).count(),
    }
