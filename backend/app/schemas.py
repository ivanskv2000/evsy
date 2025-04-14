from pydantic import BaseModel
from typing import List, Optional


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
    pass

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
