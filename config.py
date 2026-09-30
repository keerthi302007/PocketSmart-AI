from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "PocketSmart AI"
    environment: str = "development"

    secret_key: str = "change-me"

    database_url: str = "sqlite:///./data/pocketsmart.db"

    gemini_api_key: str | None = None
    gemini_model: str = "gemini-2.5-flash"

    ai_mode: str = "auto"

    allowed_origins: str = (
        "http://127.0.0.1:8000,http://localhost:8000"
    )

    session_cookie_name: str = "pocketsmart_session"

    access_token_expire_minutes: int = 60

    max_upload_mb: int = 5

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        case_sensitive=False,
    )

    @property
    def origins(self) -> list[str]:
        return [
            item.strip()
            for item in self.allowed_origins.split(",")
            if item.strip()
        ]


@lru_cache
def get_settings() -> Settings:
    return Settings()