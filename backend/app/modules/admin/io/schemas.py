from typing import Any, List, Optional

from pydantic import BaseModel

from app.modules.fields.schemas import FieldType


class ExportTag(BaseModel):
    id: str
    description: Optional[str]


class ExportField(BaseModel):
    name: str
    description: Optional[str]
    field_type: FieldType
    example: Optional[Any]


class ExportEvent(BaseModel):
    name: str
    description: Optional[str]
    links: Optional[list[dict]]
    tags: List[str]
    fields: List[str]


class ExportBundle(BaseModel):
    tags: List[ExportTag]
    fields: List[ExportField]
    events: List[ExportEvent]


class ImportBundle(ExportBundle):
    pass
