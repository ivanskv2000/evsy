from modules.events.seed.seeder import seed as seed_events
from modules.fields.seed.seeder import seed as seed_fields
from modules.tags.seed.seeder import seed as seed_tags
from sqlalchemy.orm import Session


def seed_all(db: Session):
    seed_tags(db)
    seed_fields(db)
    seed_events(db)
