from faker import Faker
from sqlalchemy.orm import Session
from app import models

fake = Faker()

def seed_tags(db: Session, tags: list[str] = None):
    tags = tags or ["feature", "experiment", "switchback", "release"]
    for tag_id in tags:
        db_tag = models.Tag(id=tag_id, description=fake.sentence())
        db.add(db_tag)
    db.commit()
