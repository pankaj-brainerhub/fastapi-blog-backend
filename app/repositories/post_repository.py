from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app.models.post import Post


class PostRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(
        self,
        post_id: int,
    ) -> Post | None:

        statement = select(Post).where(
            Post.id == post_id
        )

        return self.db.scalar(statement)

    def list(
        self,
        page: int,
        per_page: int,
        user_id: int | None = None,
        category_id: int | None = None,
        search: str | None = None,
    ) -> tuple[list[Post], int]:

        conditions = []

        if user_id is not None:
            conditions.append(
                Post.user_id == user_id
            )

        if category_id is not None:
            conditions.append(
                Post.category_id == category_id
            )

        if search:
            search_pattern = f"%{search}%"

            conditions.append(
                or_(
                    Post.title.ilike(search_pattern),
                    Post.content.ilike(search_pattern),
                )
            )

        count_statement = select(
            func.count()
        ).select_from(Post)

        if conditions:
            count_statement = count_statement.where(
                *conditions
            )

        total = self.db.scalar(
            count_statement
        ) or 0

        statement = (
            select(Post)
            .where(*conditions)
            .order_by(Post.created_at.desc())
            .offset((page - 1) * per_page)
            .limit(per_page)
        )

        posts = list(
            self.db.scalars(statement).all()
        )

        return posts, total

    def create(
        self,
        post: Post,
    ) -> Post:

        self.db.add(post)
        self.db.flush()

        return post

    def update(
        self,
        post: Post,
    ) -> Post:

        self.db.flush()

        return post

    def delete(
        self,
        post: Post,
    ) -> None:

        self.db.delete(post)
        self.db.flush()