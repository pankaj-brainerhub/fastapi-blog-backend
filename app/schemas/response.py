from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    """Standard single-item API response envelope."""

    success: bool = True
    message: str
    data: T | None = None


class PaginatedData(BaseModel, Generic[T]):
    """Paginated result payload embedded inside ApiResponse."""

    items: list[T]
    total: int
    page: int
    per_page: int
    total_pages: int


class PaginatedResponse(ApiResponse[PaginatedData[T]], Generic[T]):
    """Convenience alias: ApiResponse wrapping PaginatedData."""

    pass
