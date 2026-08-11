from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: int) -> User | None:
        statement = select(User).where(
            User.id == user_id,
            User.is_active.is_(True),
        )

        return self.db.scalar(statement)

    def get_by_email(self, email: str) -> User | None:
        statement = select(User).where(
            User.email == email,
        )

        return self.db.scalar(statement)

    def create(self, user: User) -> User:
        self.db.add(user)
        self.db.flush()

        return user

    def update(self, user: User) -> User:
        self.db.flush()

        return user

    def delete(self, user: User) -> None:
        self.db.delete(user)
        self.db.flush()

    def list(
        self,
        page: int,
        per_page: int,
        search: str | None = None,
        role_id: str | None = None,
        is_active: bool | None = None,
    ) -> tuple[list[User], int]:

        conditions = []

        if search:
            search_pattern = f"%{search}%"

            conditions.append(
                or_(
                    User.name.ilike(search_pattern),
                    User.email.ilike(search_pattern),
                )
            )

        if role_id:
            conditions.append(
                User.role_id == role_id
            )

        if is_active is not None:
            conditions.append(
                User.is_active == is_active
            )

        count_statement = select(
            func.count()
        ).select_from(User)

        if conditions:
            count_statement = count_statement.where(
                *conditions
            )

        total = self.db.scalar(count_statement) or 0

        statement = (
            select(User)
            .where(*conditions)
            .order_by(User.id.desc())
            .offset((page - 1) * per_page)
            .limit(per_page)
        )

        users = list(
            self.db.scalars(statement).all()
        )

        return users, total