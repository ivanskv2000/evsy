from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

class FieldType(str, Enum):
    string = "string"
    number = "number"
    integer = "integer"
    boolean = "boolean"
    array = "array"
    object = "object"



# Базовая схема для тега
class TagBase(BaseModel):
    id: str
    description: str | None = None

    model_config = {
        "from_attributes": True
    }

class TagCreate(TagBase):
    pass

class Tag(TagBase):
    id: str

    model_config = {
        "from_attributes": True
    }


# Базовая схема для поля
class FieldBase(BaseModel):
    name: str
    description: Optional[str] = None
    field_type: str

class FieldCreate(FieldBase):
    name: str
    field_type: FieldType

class Field(FieldBase):
    id: int

    model_config = {
        "from_attributes": True
    }


# Базовая схема для события
class EventBase(BaseModel):
    name: str
    description: Optional[str] = None
    tags: List[str] = []  # Строки, соответствующие именам тегов
    fields: List[int] = []  # Строки, соответствующие именам полей

class EventCreate(EventBase):
    pass

class Event(EventBase):
    id: int
    tags: List[Tag] = []  # Список объектов Tag
    fields: List[Field] = []  # Список объектов Field

    model_config = {
        "from_attributes": True
    }
