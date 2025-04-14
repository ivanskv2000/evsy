from sqlalchemy.orm import Session
from . import models, schemas


# Создание нового события
def create_event(db: Session, event: schemas.EventCreate):
    db_event = models.Event(
        name=event.name,
        description=event.description
    )
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


# Получение события по ID
def get_event(db: Session, event_id: int):
    return db.query(models.Event).filter(models.Event.id == event_id).first()


# Получение всех событий
def get_events(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Event).offset(skip).limit(limit).all()


# Обновление события
def update_event(db: Session, event_id: int, event: schemas.EventCreate):
    db_event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if db_event:
        db_event.name = event.name
        db_event.description = event.description
        db.commit()
        db.refresh(db_event)
        return db_event
    return None


# Удаление события
def delete_event(db: Session, event_id: int):
    db_event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if db_event:
        db.delete(db_event)
        db.commit()
        return db_event
    return None


# Создание нового тега
def create_tag(db: Session, tag: schemas.TagCreate):
    db_tag = models.Tag(id=tag.id, description=tag.description)
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag


# Получение всех тегов
def get_tags(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Tag).offset(skip).limit(limit).all()


def get_tag(db: Session, tag_id: str):
    return db.query(models.Tag).filter(models.Tag.id == tag_id).first()



# Создание нового поля
def create_field(db: Session, field: schemas.FieldCreate):
    db_field = models.Field(
        name=field.name,
        description=field.description,
        field_type=field.field_type
    )
    db.add(db_field)
    db.commit()
    db.refresh(db_field)
    return db_field


# Получение всех полей
def get_fields(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Field).offset(skip).limit(limit).all()
