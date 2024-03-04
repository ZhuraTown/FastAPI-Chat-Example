from uuid import UUID

from infrastructure.db.converters.user import convert_created_user_to_dbmodel
from infrastructure.db.repositories.user import UserRepository
from src.application.common.services import RepoService
from transfer.user import ToCreateUserDTO


class UserService(RepoService[UserRepository]):

    # todo: validation unique user
    async def register_user(self, data: ToCreateUserDTO):
        created_user = await self._repository.create_user(
            convert_created_user_to_dbmodel(data, hash_password=data.password),
        )
        return created_user

    def update_user(self, user_id, data):
        ...

    async def get_user_by_id(self, user_id):
        user = await self._repository.get_user(user_id=user_id)
        return user

    async def get_users_count(self):
        count = await self._repository.get_users_count()
        return count

    def reset_password(self, user_id, old_password, new_password):
        ...

    async def deactivate_user(self, user_id: UUID):
        await self._repository.deactivate_user(user_id)

    async def get_users(self,
                        limit: int | None = None,
                        offset: int | None = None,
                        is_active: bool | None = None,
                        ):
        users = await self._repository.get_users(limit=limit, offset=offset, is_deleted=is_active)
        return users
