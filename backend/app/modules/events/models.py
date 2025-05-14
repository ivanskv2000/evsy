from sqlalchemy import JSON, Column, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.core.models import TimestampMixin

# Required for SQLAlchemy relationship back_populates resolution
from app.shared.models import EventField, EventTag  # noqa: F401


class Event(Base, TimestampMixin):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    links = Column(JSON, nullable=True)

    tag_links = relationship(
        "EventTag", back_populates="event", cascade="all, delete-orphan"
    )
    tags = relationship(
        "Tag",
        secondary="event_tags",
        back_populates="events",
        viewonly=True,
        order_by="Tag.id.asc()",
    )

    field_links = relationship(
        "EventField", back_populates="event", cascade="all, delete-orphan"
    )
    fields = relationship(
        "Field",
        secondary="event_fields",
        back_populates="events",
        viewonly=True,
        order_by="Field.id.asc()",
    )
