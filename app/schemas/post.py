from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.constants.post import PostStatus


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

    status: PostStatus | None = None


class PostResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int
    title: str
    content: str
    status: PostStatus
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