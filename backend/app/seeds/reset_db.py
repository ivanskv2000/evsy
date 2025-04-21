from app.database import Base, engine
from sqlalchemy import MetaData

def reset_database():
    print("📂 DB URL:", engine.url)

    print("🧨 Dropping all tables...")

    meta = MetaData()
    meta.reflect(bind=engine)
    meta.drop_all(bind=engine)

    print("🛠 Recreating all tables...")
    Base.metadata.create_all(bind=engine)

    print("✅ Database reset complete.")

if __name__ == "__main__":
    reset_database()