from app.database import engine
from app import models
from sqlalchemy import MetaData

def reset_database():
    print("📂 DB URL:", engine.url)

    print("🧨 Dropping all tables...")

    meta = MetaData()
    meta.reflect(bind=engine)
    meta.drop_all(bind=engine)

    print("🛠 Recreating all tables...")
    models.Base.metadata.create_all(bind=engine)

    print("✅ Database reset complete.")

if __name__ == "__main__":
    reset_database()