from typing import Annotated

from fastapi import Depends
from fastapi_users import FastAPIUsers

from application.auth.auth import auth_backend
from presentation.api.auth.controller import fastapi_users
from transfer.user import UserDTO


def get_current_user():
    user = fastapi_users.current_user()
    return user
