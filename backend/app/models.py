from sqlalchemy import Column, Integer, String, ForeignKey, Enum, DateTime, func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .database import Base
from .schemas import FieldType
from datetime import datetime
from sqlalchemy.ext.associationproxy import association_proxy


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


# Модель для события
class Event(Base, TimestampMixin):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)

    # Связь с тегами
    tags = relationship(
        "EventTag", back_populates="event", cascade="all, delete-orphan"
    )
    tag_objects = association_proxy("tags", "tag")

    # Связь с полями
    fields = relationship("EventField", back_populates="event")
    field_objects = association_proxy("fields", "field")


# Модель для тега
class Tag(Base, TimestampMixin):
    __tablename__ = "tags"

    id = Column(String, primary_key=True, index=True)
    description = Column(String, nullable=True)

    # Связь с событиями
    events = relationship("EventTag", back_populates="tag")


# Модель для связи многие ко многим между событиями и тегами
class EventTag(Base, TimestampMixin):
    __tablename__ = "event_tags"

    event_id = Column(Integer, ForeignKey("events.id"), primary_key=True)
    tag_id = Column(String, ForeignKey("tags.id"), primary_key=True)

    # Связи с Event и Tag
    event = relationship("Event", back_populates="tags")
    tag = relationship("Tag", back_populates="events")


# Модель для поля
class Field(Base, TimestampMixin):
    __tablename__ = "fields"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String, nullable=True)
    field_type = Column(Enum(FieldType), nullable=False)

    events = relationship("EventField", back_populates="field")


# Модель для связи многие ко многим между событиями и полями
class EventField(Base, TimestampMixin):
    __tablename__ = "event_fields"

    event_id = Column(
        Integer, ForeignKey("events.id", ondelete="CASCADE"), primary_key=True
    )
    field_id = Column(
        Integer, ForeignKey("fields.id", ondelete="CASCADE"), primary_key=True
    )

    # Связи с Event и Field
    event = relationship("Event", back_populates="fields")
    field = relationship("Field", back_populates="events")
