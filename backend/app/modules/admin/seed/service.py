from sqlalchemy.orm import Session

from app.modules.events.seed.seeder import seed as seed_events
from app.modules.fields.seed.seeder import seed as seed_fields
from app.modules.tags.seed.seeder import seed as seed_tags


def seed_all(db: Session):
    seed_tags(db)
    seed_fields(db)
    seed_events(db)
