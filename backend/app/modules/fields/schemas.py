from datetime import datetime
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class FieldType(str, Enum):
    string = "string"
    number = "number"
    integer = "integer"
    boolean = "boolean"
    array = "array"
    object = "object"


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


class FieldOutWithEventCount(FieldOut):
    event_count: int
