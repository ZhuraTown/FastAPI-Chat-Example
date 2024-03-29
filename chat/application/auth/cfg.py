from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class AuthConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='AUTH_')

    SECRET_KEY: str = "SECRET_KEY"
    ALGORITHM: str = "HS256"
    ACCESS_TTL: int = 60  # seconds
    REFRESH_TTL: int = 60 * 60 * 21  # seconds


auth_settings = AuthConfig()



