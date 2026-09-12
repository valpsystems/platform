from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class TechnologyRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    slug: str = Field(..., min_length=1, max_length=200)
    category: str | None = Field(None, max_length=100)
    description: str | None = Field(None, max_length=5000)
    icon: str | None = Field(None, max_length=100)
    display_order: int = Field(default=0, ge=0, le=999)
    is_featured: bool = False
    status: str = Field(default="published", max_length=20)


class TechnologyResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    slug: str
    category: str | None = None
    description: str | None = None
    icon: str | None = None
    display_order: int = 0
    is_featured: bool = False
    status: str = "published"
    created_at: datetime
    updated_at: datetime | None = None
