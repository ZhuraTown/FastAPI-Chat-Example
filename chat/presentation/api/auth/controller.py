import uuid

from fastapi import FastAPI
from fastapi_users import FastAPIUsers

from application.services.auth import auth_backend
from chat.infrastructure.db.models.users import User


fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)