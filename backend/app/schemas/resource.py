from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ResourceRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=300)
    slug: str = Field(..., min_length=1, max_length=300)
    category: str | None = Field(None, max_length=50)
    summary: str | None = Field(None, max_length=2000)
    content: str | None = Field(None, max_length=50000)
    author: str | None = Field(None, max_length=200)
    published_date: datetime | None = None
    cover_image: str | None = Field(None, max_length=500)
    tags: str | None = Field(None, max_length=500)
    status: str = Field(default="draft", max_length=20)


class ResourceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    slug: str
    category: str | None = None
    summary: str | None = None
    content: str | None = None
    author: str | None = None
    published_date: datetime | None = None
    cover_image: str | None = None
    tags: str | None = None
    status: str = "draft"
    created_at: datetime
    updated_at: datetime | None = None
