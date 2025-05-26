from sqlalchemy.orm import Session

from app.modules.auth.models import User


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, *, email: str, hashed_pw: str) -> User:
    user = User(email=email, hashed_password=hashed_pw, is_oauth=False)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_or_create_oauth_user(db: Session, email: str, provider: str) -> User:
    user = get_user_by_email(db, email)
    if user:
        user.oauth_provider = provider
        db.commit()
        db.refresh(user)
        return user
    user = User(email=email, is_oauth=True, oauth_provider=provider)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
