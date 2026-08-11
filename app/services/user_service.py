import math

from sqlalchemy.orm import Session

from app.exceptions import (
    ConflictException,
    NotFoundException,
)
from app.repositories.user_repository import UserRepository
from app.schemas.user import (
    UserListResponse,
    UserResponse,
    UserUpdate,
)


class UserService:

    def __init__(self, db: Session):
        self.db = db
        self.repository = UserRepository(db)

    def list_users(
        self,
        page: int,
        per_page: int,
        search: str | None = None,
        role_id: str | None = None,
        is_active: bool | None = None,
    ) -> UserListResponse:

        users, total = self.repository.list(
            page=page,
            per_page=per_page,
            search=search,
            role_id=role_id,
            is_active=is_active,
        )

        total_pages = math.ceil(
            total / per_page
        ) if total else 0

        return UserListResponse(
            items=users,
            total=total,
            page=page,
            per_page=per_page,
            total_pages=total_pages,
        )

    def get_user(
        self,
        user_id: int,
    ):
        user = self.repository.get_by_id(user_id)

        if not user:
            raise NotFoundException(
                "User not found."
            )

        return user

    def update_user(
        self,
        user_id: int,
        data: UserUpdate,
    ):

        user = self.get_user(user_id)

        if data.email and data.email != user.email:
            existing_user = self.repository.get_by_email(
                data.email
            )

            if existing_user:
                raise ConflictException(
                    "Email is already registered."
                )

        update_data = data.model_dump(
            exclude_unset=True
        )

        for field, value in update_data.items():
            setattr(user, field, value)

        try:
            self.repository.update(user)

            self.db.commit()
            self.db.refresh(user)

            return user

        except Exception:
            self.db.rollback()
            raise

    def delete_user(
        self,
        user_id: int,
    ) -> None:

        user = self.get_user(user_id)

        user.is_active = False

        try:
            self.repository.update(user)

            self.db.commit()

        except Exception:
            self.db.rollback()
            raise