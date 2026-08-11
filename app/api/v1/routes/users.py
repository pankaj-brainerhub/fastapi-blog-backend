from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.dependencies import require_admin
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import (
    UserListResponse,
    UserResponse,
    UserUpdate,
)
from app.services.user_service import UserService


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get(
    "",
    response_model=UserListResponse,
)
def list_users(
    page: int = Query(
        default=1,
        ge=1,
    ),
    per_page: int = Query(
        default=10,
        ge=1,
        le=100,
    ),
    search: str | None = None,
    role_id: str | None = None,
    is_active: bool | None = None,
    _: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    service = UserService(db)

    return service.list_users(
        page=page,
        per_page=per_page,
        search=search,
        role_id=role_id,
        is_active=is_active,
    )


@router.get(
    "/{user_id}",
    response_model=UserResponse,
)
def get_user(
    user_id: int,
    _: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    service = UserService(db)

    return service.get_user(user_id)


@router.patch(
    "/{user_id}",
    response_model=UserResponse,
)
def update_user(
    user_id: int,
    data: UserUpdate,
    _: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    service = UserService(db)

    return service.update_user(
        user_id,
        data,
    )


@router.delete(
    "/{user_id}",
    status_code=204,
)
def delete_user(
    user_id: int,
    _: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    service = UserService(db)

    service.delete_user(user_id)