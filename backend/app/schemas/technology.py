from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field
from typing import Optional


class TechnologyRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    slug: str = Field(..., min_length=1, max_length=200)
    category: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = Field(None, max_length=5000)
    icon: Optional[str] = Field(None, max_length=100)
    display_order: int = Field(default=0, ge=0, le=999)
    is_featured: bool = False
    status: str = Field(default="published", max_length=20)


class TechnologyResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    slug: str
    category: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = None
    display_order: int = 0
    is_featured: bool = False
    status: str = "published"
    created_at: datetime
    updated_at: Optional[datetime] = None