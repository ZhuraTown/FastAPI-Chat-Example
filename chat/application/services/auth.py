from typing import Annotated, NoReturn

from fastapi import HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi_users.password import PasswordHelper
from passlib.context import CryptContext
from fastapi_users.authentication import BearerTransport, JWTStrategy, AuthenticationBackend
from starlette import status

from application.services.interfaces.user import UserServiceI
from presentation.api.auth.cfg import auth_settings
from presentation.api.deps.services import user_service
from transfer.user import UserDTO

context = CryptContext(schemes=["argon2", "bcrypt"], deprecated="auto")
password_helper = PasswordHelper(context)
bearer_transport = BearerTransport(tokenUrl="auth/login")


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=auth_settings.SECRET_KEY, lifetime_seconds=auth_settings.TTL)


class CustomUserAuth(AuthenticationBackend):
    """
    Mock authentication middleware. Will be deleted in the future.
    Needing of that middleware due to developing user - service earlier than authorization service.
    All users in map below must be used only as DEV environment.
    """
    TOKEN_MATCHING = {
        'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9'
        '.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkZyb250ZW5kVG9rZW5Xb3JrcyIsImlhdCI6MTUxNjIzOTAyMn0'
        '.YA9TZSAUKcMXm8U7dcNk8B5Lj4tVm4rxPE8J0eimlng': 'testsid@yandex.ru',
    }

    async def __call__(
            self,
            token: Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())],
            service: Annotated[UserServiceI, Depends(user_service)],
    ) -> UserDTO | NoReturn:
        # if (_email := self.TOKEN_MATCHING.get(token.credentials)) is None:
        #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid token')
        user = await service.get_user_by_email(_email)
        if not user:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='User with that token does not exist')
        return user


auth_backend = CustomUserAuth("chat", transport=bearer_transport, get_strategy=get_jwt_strategy)
