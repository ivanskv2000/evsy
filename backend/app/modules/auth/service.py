from fastapi import HTTPException
from passlib.context import CryptContext
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.modules.auth import crud
from app.modules.auth.schemas import UserCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def create_user(db: Session, user_in: UserCreate):
    hashed_pw = hash_password(user_in.password)
    try:
        return crud.create_user(db, email=user_in.email, hashed_pw=hashed_pw)
    except IntegrityError as err:
        db.rollback()
        raise HTTPException(
            status_code=400, detail="User with this email already exists."
        ) from err


def get_or_create_oauth_user(db: Session, email: str, provider: str):
    return crud.get_or_create_oauth_user(db, email=email, provider=provider)


def create_user_if_not_exists(db: Session, user_in: UserCreate):
    user = crud.get_user_by_email(db, user_in.email)
    if not user:
        create_user(db, user_in)
