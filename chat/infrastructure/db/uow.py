from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from application.common.exceptions import CommitError, RollbackError
from application.common.uow import UnitOfWorkI


class SQLAlchemyUoW(UnitOfWorkI):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def commit(self) -> None:
        try:
            await self._session.commit()
        except SQLAlchemyError as err:
            raise CommitError from err
        finally:
            await self._session.close()

    async def rollback(self) -> None:
        try:
            await self._session.rollback()
        except SQLAlchemyError as err:
            raise RollbackError from err
        finally:
            await self._session.close()
