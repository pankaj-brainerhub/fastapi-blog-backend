from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

import jwt

from app.core.config import get_settings
from app.db.session import get_db
from app.exceptions import UnauthorizedException
from app.models.user import User
from app.repositories.user_repository import UserRepository

from app.constants.roles import RoleEnum
from app.exceptions import ForbiddenException

settings = get_settings()

bearer_scheme = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(
        bearer_scheme
    ),
    db: Session = Depends(get_db),
) -> User:

    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )

    except jwt.InvalidTokenError:
        raise UnauthorizedException(
            "Invalid or expired token."
        )

    if payload.get("type") != "access":
        raise UnauthorizedException(
            "Invalid access token."
        )

    user_id = payload.get("sub")

    if not user_id:
        raise UnauthorizedException(
            "Invalid access token."
        )

    try:
        user_id = int(user_id)
    except (TypeError, ValueError):
        raise UnauthorizedException(
            "Invalid access token."
        )

    repository = UserRepository(db)

    user = repository.get_by_id(user_id)

    if not user:
        raise UnauthorizedException(
            "User not found."
        )

    if not user.is_active:
        raise UnauthorizedException(
            "User account is inactive."
        )

    return user


def require_admin(
    current_user: User = Depends(get_current_user),
) -> User:

    if current_user.role_id != RoleEnum.ADMIN.value:
        raise ForbiddenException()

    return current_user