from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str
    ADMIN_USERNAME: str
    ADMIN_PASSWORD_HASH: str
    SECRET_KEY: str
    ALGORITHM: str
    TOKEN_EXPIRATION_TIME: int

    model_config = SettingsConfigDict(env_file = ".env")

settings = Settings() # type: ignore