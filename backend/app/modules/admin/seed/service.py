from sqlalchemy.orm import Session

from app.modules.events.seed.seeder import seed as seed_events
from app.modules.fields.seed.seeder import seed as seed_fields
from app.modules.tags.seed.seeder import seed as seed_tags
from app.shared.service import assert_db_empty


def seed_all(db: Session, n_tags=10, n_fields=10, n_events=10):
    assert_db_empty(db)
    seed_tags(db, count=n_tags)
    seed_fields(db, count=n_fields)
    seed_events(db, count=n_events)
