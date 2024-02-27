from typing import Sequence

from infrastructure.db.converters.user import convert_user_dbmodel_to_dto
from infrastructure.db.models import User
from infrastructure.db.repositories.base import SqlAlchemyRepository, TypeS
from transfer.user import UserDTO


class UserRepository(SqlAlchemyRepository[TypeS]):

    async def create_user(self, user: User):  # todo: add tdo
        async with self._session() as session:
            session.add(user)
            await session.commit()
        return convert_user_dbmodel_to_dto(user)

    async def create_users(self, users: Sequence[User]) -> Sequence[UserDTO]:
        async with self._session() as session:
            session.add_all(users)
            await session.commit()
        return [convert_user_dbmodel_to_dto(user) for user in users]
