import logging

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.modules.admin.seed.service import seed_all
from app.modules.auth.schemas import UserCreate
from app.modules.auth.service import create_user_if_not_exists
from app.settings import Settings

logger = logging.getLogger(__name__)


def setup_test_users(db: Session, users: list[dict[str, str]]):
    """Create initial test users if they don't exist. Easily extendable."""
    for user_info in users:
        logger.info(f"Ensuring test user exists: {user_info['email']}")
        create_user_if_not_exists(db, UserCreate(**user_info))


def auto_seed_data(db: Session):
    """Seed the database with initial data if it's empty."""
    try:
        seed_all(db, n_tags=7, n_fields=12, n_events=30)
        logger.info("Auto-seeding completed successfully.")
    except HTTPException as e:
        if e.status_code == 405:
            logger.info("Database already contains data. Skipping auto-seeding.")
        else:
            logger.exception(f"Auto-seeding failed with unexpected error: {e.detail}")
    except Exception:
        logger.exception("Auto-seeding failed")


def run_startup_tasks(db: Session, settings: Settings):
    """Run all necessary startup tasks for development environment."""
    if settings.is_dev:
        setup_test_users(db, settings.dev_users)
        auto_seed_data(db)
    elif settings.is_demo:
        create_user_if_not_exists(
            db,
            UserCreate(
                email=settings.demo_user_email, password=settings.demo_user_password
            ),
        )
