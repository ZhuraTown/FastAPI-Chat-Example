from fastapi_users.authentication import JWTStrategy, AuthenticationBackend

from application.auth.hashing import bearer_transport
from application.auth.cfg import auth_settings


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=auth_settings.SECRET_KEY, lifetime_seconds=auth_settings.TTL)


auth_backend = AuthenticationBackend(name="chat", transport=bearer_transport, get_strategy=get_jwt_strategy)