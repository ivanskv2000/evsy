from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TagBase(BaseModel):
    id: str
    description: str | None = None


class TagCreate(TagBase):
    pass


class TagOut(TagBase):
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
