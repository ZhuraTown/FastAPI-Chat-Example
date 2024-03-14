from datetime import timedelta, datetime, timezone
from jose import jwt

from application.auth.cfg import auth_settings


def create_access_token_and_refresh_token(data: dict):
    access_token_data = data.copy()
    refresh_token_data = data.copy()
    expire_access = datetime.now(timezone.utc) + timedelta(seconds=auth_settings.ACCESS_TTL)
    expire_refresh = datetime.now(timezone.utc) + timedelta(seconds=auth_settings.REFRESH_TTL)
    # todo: JTI ???
    access_token_data.update({"exp": expire_access, "token_type": "access"})
    refresh_token_data.update({"exp": expire_refresh, "token_type": "refresh"})
    access_token = jwt.encode(access_token_data, auth_settings.SECRET_KEY, algorithm=auth_settings.ALGORITHM)
    refresh_token = jwt.encode(refresh_token_data, auth_settings.SECRET_KEY, algorithm=auth_settings.ALGORITHM)
    return access_token, refresh_token



# todo: logout -> add token to block list