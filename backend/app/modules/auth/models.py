from sqlalchemy import Boolean, Column, Integer, String, UniqueConstraint

from app.core.database import Base


class User(Base):
    __tablename__ = "users"
    __table_args__ = (UniqueConstraint("email", name="uq_user_email"),)

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=True)
    is_oauth = Column(Boolean, default=False)
    oauth_provider = Column(String, nullable=True)
