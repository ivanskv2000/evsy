from fastapi import HTTPException, Response
from sqlalchemy.orm import Session, joinedload

from . import models, schemas


def create_event(db: Session, event: schemas.EventCreate):
    db_event = models.Event(name=event.name, description=event.description)
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


def get_events(db: Session, skip: int = 0, limit: int = 100):
    return (
        db.query(models.Event)
        .options(
            joinedload(models.Event.tags),
            joinedload(models.Event.fields),
        )
        .offset(skip)
        .limit(limit)
        .all()
    )


def update_event(db: Session, event_id: int, event: schemas.EventCreate):
    db_event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if db_event is None:
        return None

    db_event.name = event.name
    db_event.description = event.description

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
    db_event = db.query(models.Event).filter(models.Event.id == event_id).first()

    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")

    db.delete(db_event)
    db.commit()
    return Response(status_code=204)


def create_tag(db: Session, tag: schemas.TagCreate):
    db_tag = models.Tag(id=tag.id, description=tag.description)
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag


def get_tags(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Tag).offset(skip).limit(limit).all()


def get_tag(db: Session, tag_id: str):
    return db.query(models.Tag).filter(models.Tag.id == tag_id).first()


def update_tag(db: Session, tag_id: str, tag: schemas.TagCreate):
    db_tag = db.query(models.Tag).filter(models.Tag.id == tag_id).first()
    if db_tag:
        db_tag.description = tag.description
        db.commit()
        db.refresh(db_tag)
        return db_tag
    return None


def delete_tag(db: Session, tag_id: str):
    db_tag = db.query(models.Tag).filter(models.Tag.id == tag_id).first()
    if db_tag:
        db.query(models.EventTag).filter(models.EventTag.tag_id == tag_id).delete()
        db.delete(db_tag)
        db.commit()
        return db_tag
    return None


def get_tags_by_ids(db: Session, tag_ids: list[str]):
    return db.query(models.Tag).filter(models.Tag.id.in_(tag_ids)).all()


def get_or_create_tags(db: Session, tag_ids: list[str]) -> list[models.Tag]:
    existing_tags = db.query(models.Tag).filter(models.Tag.id.in_(tag_ids)).all()
    existing_ids = {tag.id for tag in existing_tags}

    missing_ids = set(tag_ids) - existing_ids
    new_tags = [models.Tag(id=tag_id) for tag_id in missing_ids]

    if new_tags:
        db.add_all(new_tags)
        db.flush()

    return existing_tags + new_tags


def create_field(db: Session, field: schemas.FieldCreate):
    db_field = models.Field(
        name=field.name, description=field.description, field_type=field.field_type
    )
    db.add(db_field)
    db.commit()
    db.refresh(db_field)
    return db_field


def get_fields(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Field).offset(skip).limit(limit).all()


def get_field(db: Session, field_id: int):
    return db.query(models.Field).filter(models.Field.id == field_id).first()


def update_field(db: Session, field_id: int, field: schemas.FieldCreate):
    db_field = db.query(models.Field).filter(models.Field.id == field_id).first()
    if db_field:
        db_field.name = field.name
        db_field.description = field.description
        db_field.field_type = field.field_type
        db.commit()
        db.refresh(db_field)
        return db_field
    return None


def delete_field(db: Session, field_id: int):
    db_field = db.query(models.Field).filter(models.Field.id == field_id).first()
    if db_field:
        db.query(models.EventField).filter(
            models.EventField.field_id == field_id
        ).delete()
        db.delete(db_field)
        db.commit()
        return db_field
    return None


def get_fields_by_ids(db: Session, field_ids: list[int]):
    return db.query(models.Field).filter(models.Field.id.in_(field_ids)).all()
