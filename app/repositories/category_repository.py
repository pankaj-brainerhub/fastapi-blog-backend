import math

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.category import Category


class CategoryRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, category_id: int) -> Category | None:
        statement = select(Category).where(
            Category.id == category_id
        )

        return self.db.scalar(statement)

    def get_by_name(self, name: str) -> Category | None:
        statement = select(Category).where(
            func.lower(Category.name) == name.lower()
        )

        return self.db.scalar(statement)

    def list(
        self,
        page: int,
        per_page: int,
    ) -> tuple[list[Category], int]:

        count_statement = select(
            func.count()
        ).select_from(Category)

        total = self.db.scalar(count_statement) or 0

        statement = (
            select(Category)
            .order_by(Category.id.desc())
            .offset((page - 1) * per_page)
            .limit(per_page)
        )

        categories = list(
            self.db.scalars(statement).all()
        )

        return categories, total

    def create(self, category: Category) -> Category:
        self.db.add(category)
        self.db.flush()

        return category

    def update(self, category: Category) -> Category:
        self.db.flush()

        return category

    def delete(self, category: Category) -> None:
        self.db.delete(category)
        self.db.flush()