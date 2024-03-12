from typing import Protocol, Sequence
from uuid import UUID

from transfer.user import UserDTO, ToCreateUserDTO


class UserServiceI(Protocol):

    async def register_user(self, data: ToCreateUserDTO) -> UserDTO: ...

    async def update_user(self, user_id, data) -> UserDTO: ...

    async def get_user_by_id(self, user_id) -> UserDTO: ...

    async def get_user_by_email(self, email) -> UserDTO: ...

    async def get_users_count(self, is_active: bool = True) -> int: ...

    async def reset_password(self, user_id, old_password, new_password): ...

    async def deactivate_user(self, user_id: UUID): ...

    async def get_users(self,
                        limit: int | None = None,
                        offset: int | None = None,
                        is_active: bool | None = None,
                        ) -> Sequence[UserDTO]:
        ...
