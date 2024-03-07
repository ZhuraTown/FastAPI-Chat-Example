from uuid import UUID

from application.services.exceptions.user import UserWithEmailAlreadyExists
from infrastructure.db.converters.user import convert_created_user_to_dbmodel
from infrastructure.db.repositories.user import UserRepository
from src.application.common.services import RepoService
from transfer.user import ToCreateUserDTO


class UserService(RepoService[UserRepository]):

    async def register_user(self, data: ToCreateUserDTO):
        if await self._repository.get_user(email=data.email) is not None:
            raise UserWithEmailAlreadyExists(data.email)
        created_user = await self._repository.create_user(
            convert_created_user_to_dbmodel(data, hash_password=data.password),
        )
        return created_user

    # TODO:
    def update_user(self, user_id, data):
        ...

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

    async def get_users(self,
                        limit: int | None = None,
                        offset: int | None = None,
                        is_active: bool | None = None,
                        ):
        users = await self._repository.get_users(limit=limit, offset=offset, is_active=is_active)
        return users
