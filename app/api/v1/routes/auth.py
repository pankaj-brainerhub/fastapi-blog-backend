import math

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.auth import (
    LoginRequest,
    RefreshTokenRequest,
    RegisterRequest,
    TokenResponse,
    UserResponse,
)
from app.schemas.response import ApiResponse
from app.services.auth_service import AuthService


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=ApiResponse[UserResponse],
    status_code=201,
)
def register(
    data: RegisterRequest,
    db: Session = Depends(get_db),
):
    service = AuthService(db)
    user = service.register(data)

    return ApiResponse(
        message="Account created successfully.",
        data=UserResponse.model_validate(user),
    )


@router.post(
    "/login",
    response_model=ApiResponse[TokenResponse],
)
def login(
    data: LoginRequest,
    db: Session = Depends(get_db),
):
    service = AuthService(db)
    tokens = service.login(data)

    return ApiResponse(
        message="Logged in successfully.",
        data=tokens,
    )


@router.post(
    "/refresh",
    response_model=ApiResponse[TokenResponse],
)
def refresh_token(
    data: RefreshTokenRequest,
    db: Session = Depends(get_db),
):
    service = AuthService(db)
    tokens = service.refresh(data)

    return ApiResponse(
        message="Token refreshed successfully.",
        data=tokens,
    )


@router.get(
    "/me",
    response_model=ApiResponse[UserResponse],
)
def get_me(
    current_user: User = Depends(
        get_current_user
    ),
):
    return ApiResponse(
        message="User profile fetched successfully.",
        data=UserResponse.model_validate(current_user),
    )