from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class TagBase(BaseModel):
    id: str = Field(
        min_length=1,
        max_length=50,
        description="Tag ID must be between 1 and 50 characters",
    )
    description: str | None = None


class TagCreate(TagBase):
    pass


class TagOut(TagBase):
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
