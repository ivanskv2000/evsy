from passlib.context import CryptContext
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
    return crud.create_user(db, email=user_in.email, hashed_pw=hashed_pw)


def get_or_create_oauth_user(db: Session, email: str, provider: str):
    return crud.get_or_create_oauth_user(db, email=email, provider=provider)
