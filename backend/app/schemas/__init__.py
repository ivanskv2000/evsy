from datetime import datetime
from enum import Enum
from typing import List, Optional, Any

from pydantic import BaseModel, ConfigDict, Field


class FieldType(str, Enum):
    string = "string"
    number = "number"
    integer = "integer"
    boolean = "boolean"
    array = "array"
    object = "object"

class LinkType(str, Enum):
    figma = "figma"
    miro = "miro"
    confluence = "confluence"
    notion = "notion"
    loom = "loom"
    slack = "slack"
    google = "google"
    other = "other"

class EventLink(BaseModel):
    type: LinkType
    url: str
    label: Optional[str] = None


# Базовая схема для тега
class TagBase(BaseModel):
    id: str
    description: str | None = None


# Для создания
class TagCreate(TagBase):
    pass


# Для чтения из БД (в API)
class TagOut(TagBase):
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# Базовая схема для поля
class FieldBase(BaseModel):
    name: str
    description: Optional[str] = None
    field_type: FieldType
    example: Optional[Any] = None


# Для создания
class FieldCreate(FieldBase):
    pass


# Для отдачи в API
class FieldOut(FieldBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# Базовая схема для события
class EventBase(BaseModel):
    name: str
    description: Optional[str] = None
    links: Optional[List[EventLink]] = None
    tags: List[str] = []
    fields: List[int] = []


# Для создания события
class EventCreate(EventBase):
    pass


# Для ответа из API
class EventOut(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    links: Optional[List[EventLink]] = None
    tags: list[TagOut]
    fields: list[FieldOut]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
        validate_by_name = True
        )
