from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.core.models import TimestampMixin


class Tag(Base, TimestampMixin):
    __tablename__ = "tags"

    id = Column(String, primary_key=True, index=True)
    description = Column(String, nullable=True)

    events = relationship(
        "Event", secondary="event_tags", back_populates="tags", viewonly=True
    )
    tag_links = relationship(
        "EventTag", back_populates="tag", cascade="all, delete-orphan"
    )
