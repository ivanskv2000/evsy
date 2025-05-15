from sqlalchemy.orm import Session

from app.modules.events.seed.seeder import seed as seed_events
from app.modules.fields.seed.seeder import seed as seed_fields
from app.modules.tags.seed.seeder import seed as seed_tags

from app.shared.service import assert_db_empty


def seed_all(db: Session):
    assert_db_empty(db)
    seed_tags(db)
    seed_fields(db)
    seed_events(db)
