from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str
    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASSWORD: str
    OWNER_EMAIL: str
    SECRET_API_KEY: str
    ALLOWED_ORIGINS: str
    ENVIRONMENT: str = "development"

    model_config = ConfigDict(env_file=".env", extra="ignore")


settings = Settings()
