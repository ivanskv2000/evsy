from app.database.database import get_db
from app.database.seeds.seed_tags import seed_tags
from app.database.seeds.seed_fields import seed_fields
from app.database.seeds.seed_events import seed_events

def run_all_seeds():
    db_gen = get_db()
    db = next(db_gen)

    try:
        seed_tags(db)
        seed_fields(db)
        seed_events(db)
        print("🌱 All seeds completed.")
    finally:
        db_gen.close()

if __name__ == "__main__":
    run_all_seeds()
