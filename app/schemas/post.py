from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class PostCreate(BaseModel):
    title: str = Field(
        min_length=3,
        max_length=255,
    )

    content: str = Field(
        min_length=1,
    )

    category_id: int = Field(
        gt=0,
    )


class PostUpdate(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=3,
        max_length=255,
    )

    content: str | None = Field(
        default=None,
        min_length=1,
    )

    category_id: int | None = Field(
        default=None,
        gt=0,
    )


class PostResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    title: str
    content: str
    user_id: int
    category_id: int
    created_at: datetime
    updated_at: datetime


class PostListResponse(BaseModel):
    items: list[PostResponse]
    total: int
    page: int
    per_page: int
    total_pages: int