from fastapi_users.authentication import BearerTransport
from fastapi_users.password import PasswordHelper
from passlib.context import CryptContext


context = CryptContext(schemes=["argon2", "bcrypt"], deprecated="auto")
bearer_transport = BearerTransport(tokenUrl="auth/login")


def get_password_helper():
    return PasswordHelper(context)