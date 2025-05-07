from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    DATABASE_URI: str
    DATABASE_USER: str
    DATABASE_PASS: str
    DATABASE_HOST: str
    DATABASE_PORT: int
    APP_PORT: int
    LLM_SERVICE_HOST: str
    LLM_SERVICE_PORT: int
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    FERNET_CRYPT_KEY: str
    OPENROUTER_SERVICE_HOST: str

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache
def get_settings():
    return Settings()
