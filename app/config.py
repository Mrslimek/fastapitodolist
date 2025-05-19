from pydantic_settings import BaseSettings
from pathlib import Path
from datetime import timedelta
from fastapi_pagination.utils import disable_installed_extensions_check  # noqa


disable_installed_extensions_check()


BASE_DIR = Path(__file__).parent.parent


class Settings(BaseSettings):
    PG_USER: str
    PG_PASSWORD: str
    PG_DB: str
    PG_HOST: str
    PG_PORT: str
    PRIVATE_KEY_PATH: Path = BASE_DIR / "certs" / "jwt-private.pem"
    PUBLIC_KEY_PATH: Path = BASE_DIR / "certs" / "jwt-public.pem"
    ALGORITHM: str = "RS256"
    ACCESS_TOKEN_TYPE: str = "access"
    REFRESH_TOKEN_TYPE: str = "refresh"
    ACCESS_TOKEN_EXPIRE_MINUTES: timedelta = timedelta(minutes=15)
    REFRESH_TOKEN_EXPIRE_DAYS: timedelta = timedelta(days=30)

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.PG_USER}:{self.PG_PASSWORD}@{self.PG_HOST}:{self.PG_PORT}/{self.PG_DB}"

    model_config = {"env_file": BASE_DIR / ".env"}


settings = Settings()
