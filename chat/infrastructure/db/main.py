from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.exc import DatabaseError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from config import settings
from log import app_logger


class Database:
    def __init__(self) -> None:
        self.engine = create_async_engine(str(settings.infrastructure.postgres_dsn), echo=True)
        self.session_factory = async_sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

    @asynccontextmanager
    async def session(self) -> AsyncGenerator[type[AsyncSession], None]:
        async with self.session_factory() as session:
            try:
                yield session
            except DatabaseError as e:
                app_logger.error(f'Transaction failed: {e}')
                await session.rollback()
            finally:
                await session.close()

    async def uow_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.session_factory() as session:
            yield session


db = Database()
