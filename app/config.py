"""Application configuration management."""

from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    # Database
    DATABASE_URL: str = "postgresql://brain_capital:changeme@localhost:5432/brain_capital_db"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # Application
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "info"
    DEBUG: bool = True

    # CORS
    ALLOWED_ORIGINS: str = "http://localhost:3000,http://localhost:8000"

    @property
    def allowed_origins_list(self) -> list[str]:
        """Parse ALLOWED_ORIGINS into a list."""
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]

    # API Keys (Future)
    OPENAI_API_KEY: str | None = None
    HUGGINGFACE_API_KEY: str | None = None
    AI_MODEL: str = "gpt-4"

    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60

    class Config:
        """Pydantic configuration."""
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # Ignore extra env vars (like POSTGRES_USER for Docker)


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


settings = get_settings()
