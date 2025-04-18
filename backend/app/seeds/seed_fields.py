from faker import Faker
from sqlalchemy.orm import Session
from app import models

fake = Faker()

def seed_fields(db: Session, count: int = 20):
    for _ in range(count):
        db_field = models.Field(
            name=fake.unique.slug(),
            description=fake.sentence(),
            field_type=fake.enum(models.FieldType)
        )
        db.add(db_field)
    db.commit()
