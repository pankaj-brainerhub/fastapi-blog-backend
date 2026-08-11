from sqlalchemy.orm import Session

from app.constants.roles import RoleEnum
from app.core.security import hash_password
from app.exceptions import ConflictException
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate


class AuthService:

    def __init__(self, db: Session):
        self.db = db
        self.user_repository = UserRepository(db)

    def register(self, data: UserCreate) -> User:

        existing_user = self.user_repository.get_by_email(
            data.email
        )

        if existing_user:
            raise ConflictException(
                "Email is already registered."
            )

        user = User(
            role_id=RoleEnum.USER.value,
            name=data.name,
            email=data.email,
            password=hash_password(data.password),
        )

        try:
            self.user_repository.create(user)

            self.db.commit()
            self.db.refresh(user)

            return user

        except Exception:
            self.db.rollback()
            raise