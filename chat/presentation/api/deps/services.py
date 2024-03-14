from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from application.services.interfaces.user import UserServiceI
from application.services.user import UserService
from infrastructure.db.main import db
from infrastructure.db.repositories.user import UserRepository
from infrastructure.db.uow import SQLAlchemyUoW
from transfer.user import UserDTO


def user_service(
        session: Annotated[AsyncSession, Depends(db.uow_session)],
) -> UserServiceI:
    return UserService(
        repository=UserRepository(session=session),
        uow=SQLAlchemyUoW(session=session)
    )

