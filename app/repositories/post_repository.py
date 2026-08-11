from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app.constants.post import PostStatus
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
        status: PostStatus | None = None,
        search: str | None = None,
        sort_by: str = "created_at",
        sort_order: str = "desc",
    ) -> tuple[list[Post], int]:

        conditions = []

        # Ownership filtering
        if user_id is not None:
            conditions.append(
                Post.user_id == user_id
            )

        # Category filtering
        if category_id is not None:
            conditions.append(
                Post.category_id == category_id
            )

        # Status filtering
        if status is not None:
            conditions.append(
                Post.status == status
            )

        # Search title + content
        if search:
            search_pattern = f"%{search}%"

            conditions.append(
                or_(
                    Post.title.ilike(search_pattern),
                    Post.content.ilike(search_pattern),
                )
            )

        # -------------------------
        # Count
        # -------------------------

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

        # -------------------------
        # Sorting
        # -------------------------

        sort_columns = {
            "id": Post.id,
            "title": Post.title,
            "created_at": Post.created_at,
            "updated_at": Post.updated_at,
            "status": Post.status,
        }

        sort_column = sort_columns.get(
            sort_by,
            Post.created_at,
        )

        if sort_order.lower() == "asc":
            order_clause = sort_column.asc()
        else:
            order_clause = sort_column.desc()

        # -------------------------
        # Data query
        # -------------------------

        statement = (
            select(Post)
            .where(*conditions)
            .order_by(order_clause)
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