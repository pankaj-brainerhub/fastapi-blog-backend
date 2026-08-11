import math

from sqlalchemy.orm import Session

from app.exceptions import NotFoundException
from app.models.post import Post
from app.repositories.category_repository import CategoryRepository
from app.repositories.post_repository import PostRepository
from app.schemas.post import (
    PostCreate,
    PostListResponse,
    PostUpdate,
)


class PostService:

    def __init__(self, db: Session):
        self.db = db
        self.repository = PostRepository(db)
        self.category_repository = CategoryRepository(db)

    def create(
        self,
        data: PostCreate,
        user_id: int,
    ) -> Post:

        category = self.category_repository.get_by_id(
            data.category_id
        )

        if not category:
            raise NotFoundException(
                "Category not found."
            )

        post = Post(
            title=data.title,
            content=data.content,
            user_id=user_id,
            category_id=data.category_id,
        )

        try:
            self.repository.create(post)

            self.db.commit()
            self.db.refresh(post)

            return post

        except Exception:
            self.db.rollback()
            raise

    def get(
        self,
        post_id: int,
    ) -> Post:

        post = self.repository.get_by_id(
            post_id
        )

        if not post:
            raise NotFoundException(
                "Post not found."
            )

        return post

    def list(
        self,
        page: int,
        per_page: int,
        user_id: int | None = None,
        category_id: int | None = None,
        search: str | None = None,
    ) -> PostListResponse:

        posts, total = self.repository.list(
            page=page,
            per_page=per_page,
            user_id=user_id,
            category_id=category_id,
            search=search,
        )

        total_pages = (
            math.ceil(total / per_page)
            if total
            else 0
        )

        return PostListResponse(
            items=posts,
            total=total,
            page=page,
            per_page=per_page,
            total_pages=total_pages,
        )

    def update(
        self,
        post_id: int,
        data: PostUpdate,
    ) -> Post:

        post = self.get(post_id)

        if data.category_id is not None:

            category = (
                self.category_repository.get_by_id(
                    data.category_id
                )
            )

            if not category:
                raise NotFoundException(
                    "Category not found."
                )

        update_data = data.model_dump(
            exclude_unset=True
        )

        for field, value in update_data.items():
            setattr(post, field, value)

        try:
            self.repository.update(post)

            self.db.commit()
            self.db.refresh(post)

            return post

        except Exception:
            self.db.rollback()
            raise

    def delete(
        self,
        post_id: int,
    ) -> None:

        post = self.get(post_id)

        try:
            self.repository.delete(post)

            self.db.commit()

        except Exception:
            self.db.rollback()
            raise