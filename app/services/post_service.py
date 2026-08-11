import math

from sqlalchemy.orm import Session

from app.constants.post import PostStatus
from app.exceptions import ForbiddenException, NotFoundException
from app.models.post import Post
from app.models.user import User
from app.repositories.category_repository import CategoryRepository
from app.repositories.post_repository import PostRepository
from app.constants.roles import RoleEnum
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

    # ---------------------------------------------------------
    # Create
    # ---------------------------------------------------------

    def create(
        self,
        data: PostCreate,
        current_user: User,
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
            user_id=current_user.id,
            category_id=data.category_id,
            status=PostStatus.DRAFT,
        )

        try:
            self.repository.create(post)

            self.db.commit()
            self.db.refresh(post)

            return post

        except Exception:
            self.db.rollback()
            raise

    # ---------------------------------------------------------
    # Get single post
    # ---------------------------------------------------------

    def get(
        self,
        post_id: int,
        current_user: User,
    ) -> Post:

        post = self.repository.get_by_id(
            post_id
        )

        if not post:
            raise NotFoundException(
                "Post not found."
            )

        self._check_ownership(
            post,
            current_user,
        )

        return post

    # ---------------------------------------------------------
    # List posts
    # ---------------------------------------------------------

    def list(
        self,
        page: int,
        per_page: int,
        current_user: User,
        category_id: int | None = None,
        status: PostStatus | None = None,
        search: str | None = None,
        sort_by: str = "created_at",
        sort_order: str = "desc",
    ) -> PostListResponse:

        # Standard users only see their own posts.
        # Admins can see all posts.
        user_id = self._get_owner_filter(
            current_user
        )

        posts, total = self.repository.list(
            page=page,
            per_page=per_page,
            user_id=user_id,
            category_id=category_id,
            status=status,
            search=search,
            sort_by=sort_by,
            sort_order=sort_order,
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

    # ---------------------------------------------------------
    # Update
    # ---------------------------------------------------------

    def update(
        self,
        post_id: int,
        data: PostUpdate,
        current_user: User,
    ) -> Post:

        post = self.repository.get_by_id(
            post_id
        )

        if not post:
            raise NotFoundException(
                "Post not found."
            )

        self._check_ownership(
            post,
            current_user,
        )

        update_data = data.model_dump(
            exclude_unset=True
        )

        # Validate category if it is being changed.
        if "category_id" in update_data:

            category = (
                self.category_repository.get_by_id(
                    update_data["category_id"]
                )
            )

            if not category:
                raise NotFoundException(
                    "Category not found."
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

    # ---------------------------------------------------------
    # Delete
    # ---------------------------------------------------------

    def delete(
        self,
        post_id: int,
        current_user: User,
    ) -> None:

        post = self.repository.get_by_id(
            post_id
        )

        if not post:
            raise NotFoundException(
                "Post not found."
            )

        self._check_ownership(
            post,
            current_user,
        )

        try:
            self.repository.delete(post)

            self.db.commit()

        except Exception:
            self.db.rollback()
            raise

    # ---------------------------------------------------------
    # Ownership helpers
    # ---------------------------------------------------------

    def _get_owner_filter(
        self,
        current_user: User,
    ) -> int | None:

        if current_user.role_id == RoleEnum.ADMIN.value:
            return None

        return current_user.id

    def _check_ownership(
        self,
        post: Post,
        current_user: User,
    ) -> None:

        # Admin can access any post.
        if current_user.role_id == RoleEnum.ADMIN.value:
            return

        # Standard user can access only their own post.
        if post.user_id != current_user.id:
            raise ForbiddenException(
                "You do not have permission to access this post."
            )