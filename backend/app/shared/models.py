from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.core.models import TimestampMixin


class EventTag(Base, TimestampMixin):
    __tablename__ = "event_tags"

    event_id = Column(Integer, ForeignKey("events.id"), primary_key=True)
    tag_id = Column(String, ForeignKey("tags.id"), primary_key=True)

    event = relationship("Event", back_populates="tag_links")
    tag = relationship("Tag", back_populates="tag_links")


class EventField(Base, TimestampMixin):
    __tablename__ = "event_fields"

    event_id = Column(
        Integer, ForeignKey("events.id", ondelete="CASCADE"), primary_key=True
    )
    field_id = Column(
        Integer, ForeignKey("fields.id", ondelete="CASCADE"), primary_key=True
    )

    event = relationship("Event", back_populates="field_links")
    field = relationship("Field", back_populates="field_links")
