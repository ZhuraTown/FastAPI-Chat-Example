from typing import Optional
from uuid import UUID

from fastapi.security import OAuth2PasswordRequestForm

from application.services.exceptions.user import UserWithEmailAlreadyExists
from application.auth.hashing import get_password_hash, verify_password_and_update
from infrastructure.db.converters.user import convert_created_user_to_dbmodel
from infrastructure.db.repositories.user import UserRepository
from chat.application.common.services import UowRepoService
from transfer.user import ToCreateUserDTO, UserDTO, UpdatedUserData


class UserService(UowRepoService[UserRepository]):

    async def register_user(self, data: ToCreateUserDTO):
        if await self._repository.get_user(email=data.email) is not None:
            raise UserWithEmailAlreadyExists(data.email)

        created_user = await self._repository.create_user(
            convert_created_user_to_dbmodel(data, hash_password=get_password_hash(data.password)),
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

    async def get_user_by_email(self, email) -> UserDTO:
        user = await self._repository.get_user(email=email)
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

    async def authenticate(
            self, credentials: OAuth2PasswordRequestForm
    ) -> Optional[UserDTO]:
        user = await self._repository.get_user(email=credentials.username)
        if not user:
            # Run the hasher to mitigate timing attack
            # Inspired from Django: https://code.djangoproject.com/ticket/20760
            get_password_hash(credentials.password)
            return None

        verified, updated_password_hash = verify_password_and_update(
            credentials.password, user.hashed_password
        )
        if not verified:
            return None
        # Update password hash to a more robust one if needed
        # todo: check how work
        if updated_password_hash is not None:
            await self._repository.update_user(user.id, {"hashed_password": updated_password_hash})
        return user

