import uuid

from fastapi_users import FastAPIUsers

from application.auth.auth import auth_backend
from application.services.user import get_user_manager
from chat.infrastructure.db.models.users import User


fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)

auth_router = fastapi_users.get_auth_router(auth_backend)