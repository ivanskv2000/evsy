from datetime import datetime

from sqlalchemy import (
    JSON,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base
from app.schemas import FieldType


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


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
    )

    field_links = relationship(
        "EventField", back_populates="event", cascade="all, delete-orphan"
    )
    fields = relationship(
        "Field",
        secondary="event_fields",
        back_populates="events",
        viewonly=True,
    )


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


class EventTag(Base, TimestampMixin):
    __tablename__ = "event_tags"

    event_id = Column(Integer, ForeignKey("events.id"), primary_key=True)
    tag_id = Column(String, ForeignKey("tags.id"), primary_key=True)

    event = relationship("Event", back_populates="tag_links")
    tag = relationship("Tag", back_populates="tag_links")


class Field(Base, TimestampMixin):
    __tablename__ = "fields"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String, nullable=True)
    field_type = Column(Enum(FieldType), nullable=False)
    example = Column(JSON, nullable=True)

    events = relationship(
        "Event", secondary="event_fields", back_populates="fields", viewonly=True
    )
    field_links = relationship(
        "EventField", back_populates="field", cascade="all, delete-orphan"
    )


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
