from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from starlette import status

from application.auth.cfg import auth_settings
from application.services.interfaces.user import UserServiceI
from presentation.api.deps.services import user_service

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        service: Annotated[UserServiceI, Depends(user_service)]
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, auth_settings.SECRET_KEY, algorithms=[auth_settings.ALGORITHM])
        user_email: str = payload.get("sub")
        if user_email is None or payload.get('token_type') != "access":
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await service.get_user_by_email(user_email)
    if user is None:
        raise credentials_exception
    return user
