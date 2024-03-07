import datetime
from typing import Sequence
from uuid import UUID

from sqlalchemy import Select, select, and_, func, Update, update

from infrastructure.db.converters.user import convert_user_dbmodel_to_dto
from infrastructure.db.models import User
from infrastructure.db.repositories.base import SqlAlchemyRepository, S
from transfer.user import UserDTO, UpdatedUserData


class UserRepository(SqlAlchemyRepository[S]):

    async def create_user(self, user: User):
        self._session.add(user)
        await self._session.flush()
        return convert_user_dbmodel_to_dto(user)

    async def create_users(self, users: Sequence[User]) -> Sequence[UserDTO]:
        self._session.add_all(users)
        await self._session.flush()
        return [convert_user_dbmodel_to_dto(user) for user in users]

    async def get_user(self,
                       user_id: UUID | None = None,
                       email: str | None = None,
                       is_active: bool | None = True,
                       # TODO: optional fields?? for search
                       ):
        filters = {
            User.id: user_id,
            User.email: email,
            User.is_active: is_active
        }
        query: Select = (
            select(User)
            .where(and_(*[k == v for k, v in filters.items() if v is not None]))
        )
        user = await self._session.scalar(query)
        return convert_user_dbmodel_to_dto(user)

    async def deactivate_user(self,
                              user_id: UUID,
                              ):
        query: Update = (
            update(User)
            .where(
                User.id == user_id,
            )
            .values(
                is_active=False,
                deleted_at=datetime.datetime.now()
            )
        )

        await self._session.execute(query)
        await self._session.flush()

    async def get_users_count(self, is_active: bool | None = None):
        query: Select = (
            select(func.count())
            .select_from(User)
        )
        if is_active is not None:
            query = query.where(User.is_active.is_(is_active))

        count = await self._session.execute(query)
        return count.scalar_one()

    async def get_users(self,
                        limit: int | None = None,
                        offset: int | None = None,
                        is_active: bool | None = None):
        query: Select = (
            select(User)
            .limit(limit)
            .offset(offset)
            .order_by(User.created_at)
        )
        if is_active is not None:
            query = query.filter(User.is_active.is_(is_active))

        users = await self._session.scalars(query)
        return tuple([convert_user_dbmodel_to_dto(user) for user in users.all()])

    async def update_user(
            self,
            user_id: UUID,
            update_data: UpdatedUserData
    ) -> UserDTO:
        query: Update = (
            update(User)
            .where(User.id == user_id)
            .values(**update_data)
        )
        await self._session.execute(query)
        await self._session.flush()
        return await self.get_user(user_id=user_id)











