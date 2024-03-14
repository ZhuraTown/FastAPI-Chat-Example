from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from application.auth.auth import create_access_token_and_refresh_token
from application.auth.errors import ErrorCode
from application.services.interfaces.user import UserServiceI
from presentation.api.auth.responses import Token
from presentation.api.deps.services import user_service


router = APIRouter(
    prefix="/auth",
    tags=["users"],
)


@router.post(
    "/login",
    name="auth:chat",
    response_model=Token
)
async def login(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        service: Annotated[UserServiceI, Depends(user_service)],
):
    user = await service.authenticate(form_data)

    if user is None or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorCode.LOGIN_BAD_CREDENTIALS,
        )
    access_token, refresh_token = create_access_token_and_refresh_token(data={"sub": user.email})
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

