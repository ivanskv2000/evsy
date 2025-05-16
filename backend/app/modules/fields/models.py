from sqlalchemy import JSON, Column, Enum, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.core.models import TimestampMixin
from app.modules.fields.schemas import FieldType


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
