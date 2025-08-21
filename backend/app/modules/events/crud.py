from sqlalchemy.orm import Session, joinedload

from . import models, schemas


def create_event(db: Session, event: schemas.EventCreate):
    db_event = models.Event(
        name=event.name,
        description=event.description,
        links=[link.model_dump() for link in event.links] if event.links else [],
    )
    db.add(db_event)
    db.commit()
    db.refresh(db_event)

    for tag_id in event.tags:
        db.add(models.EventTag(event_id=db_event.id, tag_id=tag_id))

    for field_id in event.fields:
        db.add(models.EventField(event_id=db_event.id, field_id=field_id))

    db.commit()
    db.refresh(db_event)
    return db_event


def get_event(db: Session, event_id: int):
    return db.query(models.Event).filter(models.Event.id == event_id).first()


def get_events(db: Session):
    return (
        db.query(models.Event)
        .options(
            joinedload(models.Event.tags),
            joinedload(models.Event.fields),
        )
        .order_by(models.Event.id)
        .all()
    )


def update_event(db: Session, event_id: int, event: schemas.EventCreate):
    db_event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if db_event is None:
        return None

    db_event.name = event.name
    db_event.description = event.description
    db_event.links = [link.model_dump() for link in event.links] if event.links else []

    if event.tags is not None:
        db.query(models.EventTag).filter(
            models.EventTag.event_id == db_event.id
        ).delete()
        if event.tags:
            for tag_id in event.tags:
                db.add(models.EventTag(event_id=db_event.id, tag_id=tag_id))

    if event.fields is not None:
        db.query(models.EventField).filter(
            models.EventField.event_id == db_event.id
        ).delete()
        if event.fields:
            for field_id in event.fields:
                db.add(models.EventField(event_id=db_event.id, field_id=field_id))

    db.commit()
    db.refresh(db_event)
    return db_event


def delete_event(db: Session, event_id: int):
    db_event = (
        db.query(models.Event)
        .options(
            joinedload(models.Event.tags),
            joinedload(models.Event.fields),
        )
        .filter(models.Event.id == event_id)
        .first()
    )
    if db_event:
        db.delete(db_event)
        db.commit()
        return db_event
    return None
