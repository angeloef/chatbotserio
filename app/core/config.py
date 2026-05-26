"""Application settings from environment variables."""

from typing import Any

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """ChatbotSerio configuration loaded from environment."""

    # Application
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "DEBUG"
    APP_NAME: str = "ChatbotSerio"

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://chatbotserio:chatbotserio@localhost:5432/chatbotserio"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # LLM
    OPENAI_API_KEY: str = ""
    LLM_MODEL: str = "gpt-5.4-mini"

    @property
    def DATABASE_ENGINE_KWARGS(self) -> dict[str, Any]:
        """Engine kwargs: pool only for PostgreSQL, skip for SQLite."""
        if "sqlite" in self.DATABASE_URL:
            return {"connect_args": {"check_same_thread": False}}
        return {"pool_size": 10, "max_overflow": 20}

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
