from sqlalchemy.orm import Session
from app import models
from faker import Faker
import random

faker = Faker()

def seed_events(db: Session, count: int = 10):
    tags = db.query(models.Tag).all()
    fields = db.query(models.Field).all()

    if not tags or not fields:
        print("⚠️ No tags or fields available. Please seed them first.")
        return

    for _ in range(count):
        event = models.Event(
            name=faker.unique.slug(),
            description=faker.sentence(),
        )
        db.add(event)
        db.commit()
        db.refresh(event)

        # Привязка случайных тегов
        for tag in random.sample(tags, k=min(2, len(tags))):
            db.add(models.EventTag(event_id=event.id, tag_id=tag.id))

        # Привязка случайных полей
        for field in random.sample(fields, k=min(3, len(fields))):
            db.add(models.EventField(event_id=event.id, field_id=field.id))

        db.commit()

    print(f"✅ Seeded {count} events with random tags and fields.")
