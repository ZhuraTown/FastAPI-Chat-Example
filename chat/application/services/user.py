import uuid
from typing import Optional
from uuid import UUID

from fastapi import Depends
from fastapi_users import UUIDIDMixin, BaseUserManager
from starlette.requests import Request

from application.services.exceptions.user import UserWithEmailAlreadyExists
from application.auth.hashing import get_password_helper
from infrastructure.db.converters.user import convert_created_user_to_dbmodel
from infrastructure.db.models import User
from infrastructure.db.models.users import get_user_db
from infrastructure.db.repositories.user import UserRepository
from chat.application.common.services import UowRepoService
from application.auth.cfg import auth_settings
from transfer.user import ToCreateUserDTO, UserDTO, UpdatedUserData


class UserService(UowRepoService[UserRepository]):

    async def register_user(self, data: ToCreateUserDTO):
        if await self._repository.get_user(email=data.email) is not None:
            raise UserWithEmailAlreadyExists(data.email)

        created_user = await self._repository.create_user(
            convert_created_user_to_dbmodel(data, hash_password=get_password_helper().hash(data.password)),
        )
        await self._uow.commit()
        return created_user

    async def update_user(
            self,
            user: UserDTO,
            update_data: UpdatedUserData
    ) -> UserDTO:

        updated_user = await self._repository.update_user(user_id=user.id, update_data=update_data)
        await self._uow.commit()
        return updated_user

    async def get_user_by_id(self, user_id):
        user = await self._repository.get_user(user_id=user_id)
        return user

    async def get_users_count(self, is_active: bool = True) -> int:
        count = await self._repository.get_users_count(is_active)
        return count

    # TODO:
    def reset_password(self, user_id, old_password, new_password):
        ...

    async def deactivate_user(self, user_id: UUID):
        await self._repository.deactivate_user(user_id)
        await self._uow.commit()

    async def get_users(self,
                        limit: int | None = None,
                        offset: int | None = None,
                        is_active: bool | None = None,
                        ):
        users = await self._repository.get_users(limit=limit, offset=offset, is_active=is_active)
        return users


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = auth_settings.SECRET_KEY
    verification_token_secret = auth_settings.SECRET_KEY

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
            self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
            self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"Verification requested for user {user.id}. Verification token: {token}")


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db, password_helper=get_password_helper())
