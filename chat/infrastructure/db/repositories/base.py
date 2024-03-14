from abc import ABC
from typing import Generic, Type, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.db.main import db

_S = TypeVar('_S')

TypeS = Type[AsyncSession]
S = AsyncSession


class SqlAlchemyRepository(Generic[_S], ABC):
    def __init__(self, session=None):
        self._session: _S = ...

        if not session:
            self._session: _S = db.session
        else:
            self._session: _S = session
