from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field
from typing import Optional


class ResourceRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=300)
    slug: str = Field(..., min_length=1, max_length=300)
    category: Optional[str] = Field(None, max_length=50)
    summary: Optional[str] = Field(None, max_length=2000)
    content: Optional[str] = Field(None, max_length=50000)
    author: Optional[str] = Field(None, max_length=200)
    published_date: Optional[datetime] = None
    cover_image: Optional[str] = Field(None, max_length=500)
    tags: Optional[str] = Field(None, max_length=500)
    status: str = Field(default="draft", max_length=20)


class ResourceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    slug: str
    category: Optional[str] = None
    summary: Optional[str] = None
    content: Optional[str] = None
    author: Optional[str] = None
    published_date: Optional[datetime] = None
    cover_image: Optional[str] = None
    tags: Optional[str] = None
    status: str = "draft"
    created_at: datetime
    updated_at: Optional[datetime] = None