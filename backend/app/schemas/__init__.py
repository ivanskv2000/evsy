from datetime import datetime
from enum import Enum
from typing import Any, List, Optional

from pydantic import BaseModel, ConfigDict


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


class TagBase(BaseModel):
    id: str
    description: str | None = None


class TagCreate(TagBase):
    pass


class TagOut(TagBase):
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class FieldBase(BaseModel):
    name: str
    description: Optional[str] = None
    field_type: FieldType
    example: Optional[Any] = None


class FieldCreate(FieldBase):
    pass


class FieldOut(FieldBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class EventBase(BaseModel):
    name: str
    description: Optional[str] = None
    links: Optional[List[EventLink]] = None
    tags: List[str] = []
    fields: List[int] = []


class EventCreate(EventBase):
    pass


class EventOut(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    links: Optional[List[EventLink]] = None
    tags: list[TagOut]
    fields: list[FieldOut]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True, validate_by_name=True)
