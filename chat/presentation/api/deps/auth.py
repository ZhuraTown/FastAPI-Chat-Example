from typing import Annotated

from fastapi import Depends

from application.services.auth import auth_backend
from transfer.user import UserDTO


def get_current_user(user: Annotated[UserDTO, Depends(auth_backend)]):
    return user
