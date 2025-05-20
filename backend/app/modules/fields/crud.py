from sqlalchemy import func
from sqlalchemy.orm import Session

from app.shared.models import EventField

from . import models, schemas


def create_field(db: Session, field: schemas.FieldCreate):
    db_field = models.Field(
        name=field.name, description=field.description, field_type=field.field_type
    )
    db.add(db_field)
    db.commit()
    db.refresh(db_field)
    return db_field


def get_fields(db: Session):
    return db.query(models.Field).order_by(models.Field.id).all()


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
            EventField.field_id == field_id
        ).delete()
        db.delete(db_field)
        db.commit()
        return db_field
    return None


def get_field_event_count(db: Session, field_id: int):
    return (
        db.query(func.count(EventField.event_id))
        .filter(EventField.field_id == field_id)
        .scalar()
    )


def get_fields_by_ids(db: Session, field_ids: list[int]):
    return db.query(models.Field).filter(models.Field.id.in_(field_ids)).all()
