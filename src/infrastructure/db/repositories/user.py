import datetime
from typing import Sequence
from uuid import UUID

from sqlalchemy import Select, select, and_, func, Update, update

from infrastructure.db.converters.user import convert_user_dbmodel_to_dto
from infrastructure.db.models import User
from infrastructure.db.repositories.base import SqlAlchemyRepository, TypeS
from transfer.user import UserDTO


class UserRepository(SqlAlchemyRepository[TypeS]):

    async def create_user(self, user: User):
        async with self._session() as session:
            session.add(user)
            await session.commit()
        return convert_user_dbmodel_to_dto(user)

    async def create_users(self, users: Sequence[User]) -> Sequence[UserDTO]:
        async with self._session() as session:
            session.add_all(users)
            await session.commit()
        return [convert_user_dbmodel_to_dto(user) for user in users]

    async def get_user(self,
                       user_id: UUID | None = None,
                       email: str | None = None,
                       # TODO: optional fields??
                       ):
        filters = {
            User.id: user_id,
            User.email: email
        }
        query: Select = (
            select(User)
            .where(and_(*[k == v for k, v in filters.items() if v is not None]))
        )
        async with self._session() as session:
            user = await session.scalar(query)
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
        async with self._session() as session:
            await session.execute(query)
            await session.commit()

    async def get_users_count(self, is_deleted: bool | None = None):
        query: Select = (
            select(func.count())
            .select_from(User)
        )
        if is_deleted:
            query.where(User.is_active.is_(True))

        async with self._session() as session:
            count = await session.execute(query)
        return count.scalar_one()

    async def get_users(self,
                        limit: int | None = None,
                        offset: int | None = None,
                        is_deleted: bool | None = None):
        query: Select = (
            select(User)
            .limit(limit)
            .offset(offset)
            .order_by(User.created_at)
        )
        if is_deleted:
            query.where(User.is_active.is_(True))

        async with self._session() as session:
            users = await session.scalars(query)
        return [convert_user_dbmodel_to_dto(user) for user in users.all()]










