from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, ConfigDict

from app.modules.fields.schemas import FieldOut
from app.modules.tags.schemas import TagOut


class LinkType(str, Enum):
    figma = "figma"
    miro = "miro"
    confluence = "confluence"
    jira = "jira"
    notion = "notion"
    loom = "loom"
    slack = "slack"
    google = "google"
    other = "other"


class EventLink(BaseModel):
    type: LinkType
    url: str
    label: Optional[str] = None

    model_config = ConfigDict(exclude_none=False)


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
