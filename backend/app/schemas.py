from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


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
    tags: List[str] = []  # Список slug'ов тегов
    fields: List[int] = []  # Список ID полей


# Для создания события
class EventCreate(EventBase):
    pass


# Для ответа из API
class EventOut(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    tags: list[TagOut] = Field(alias="tag_objects")
    fields: list[FieldOut] = Field(alias="field_objects")
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
