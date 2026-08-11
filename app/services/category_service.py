import math

from sqlalchemy.orm import Session

from app.exceptions import (
    ConflictException,
    NotFoundException,
)
from app.models.category import Category
from app.repositories.category_repository import CategoryRepository
from app.schemas.category import (
    CategoryCreate,
    CategoryListResponse,
    CategoryUpdate,
)


class CategoryService:

    def __init__(self, db: Session):
        self.db = db
        self.repository = CategoryRepository(db)

    def create(
        self,
        data: CategoryCreate,
    ) -> Category:

        existing_category = self.repository.get_by_name(
            data.name
        )

        if existing_category:
            raise ConflictException(
                "Category already exists."
            )

        category = Category(
            name=data.name,
        )

        try:
            self.repository.create(category)

            self.db.commit()
            self.db.refresh(category)

            return category

        except Exception:
            self.db.rollback()
            raise

    def list(
        self,
        page: int,
        per_page: int,
    ) -> CategoryListResponse:

        categories, total = self.repository.list(
            page=page,
            per_page=per_page,
        )

        total_pages = (
            math.ceil(total / per_page)
            if total
            else 0
        )

        return CategoryListResponse(
            items=categories,
            total=total,
            page=page,
            per_page=per_page,
            total_pages=total_pages,
        )

    def get(
        self,
        category_id: int,
    ) -> Category:

        category = self.repository.get_by_id(
            category_id
        )

        if not category:
            raise NotFoundException(
                "Category not found."
            )

        return category

    def update(
        self,
        category_id: int,
        data: CategoryUpdate,
    ) -> Category:

        category = self.get(category_id)

        update_data = data.model_dump(
            exclude_unset=True
        )

        if "name" in update_data:
            existing_category = (
                self.repository.get_by_name(
                    update_data["name"]
                )
            )

            if (
                existing_category
                and existing_category.id != category.id
            ):
                raise ConflictException(
                    "Category already exists."
                )

        for field, value in update_data.items():
            setattr(category, field, value)

        try:
            self.repository.update(category)

            self.db.commit()
            self.db.refresh(category)

            return category

        except Exception:
            self.db.rollback()
            raise

    def delete(
        self,
        category_id: int,
    ) -> None:

        category = self.get(category_id)

        try:
            self.repository.delete(category)

            self.db.commit()

        except Exception:
            self.db.rollback()
            raise