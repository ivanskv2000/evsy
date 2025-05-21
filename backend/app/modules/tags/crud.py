from sqlalchemy.orm import Session

from app.shared.models import EventTag

from . import models, schemas


def create_tag(db: Session, tag: schemas.TagCreate):
    db_tag = models.Tag(id=tag.id, description=tag.description)
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag


def get_tags(db: Session):
    return (
        db.query(models.Tag).order_by(models.Tag.created_at.desc(), models.Tag.id).all()
    )


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
        db.query(EventTag).filter(EventTag.tag_id == tag_id).delete()
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
