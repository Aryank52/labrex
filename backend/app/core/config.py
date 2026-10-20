from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import List


class Settings(BaseSettings):
    """Authoritative LABREX platform settings and environment validation."""
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    # Core Application
    APP_NAME: str = "LABREX Intelligence Platform"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = Field(default="LOCAL", description="LOCAL, STAGING, or PRODUCTION")
    DEBUG: bool = Field(default=False)
    API_V1_PREFIX: str = "/api/v1"

    # Database Configuration
    DATABASE_URL: str = Field(
        default="postgresql+asyncpg://postgres:postgres@localhost:5432/labrex_db",
        description="Async SQLAlchemy database connection string"
    )
    DB_POOL_SIZE: int = Field(default=10)
    DB_MAX_OVERFLOW: int = Field(default=20)
    DB_POOL_TIMEOUT: int = Field(default=30)

    # Security & Authentication
    JWT_SECRET_KEY: str = Field(
        default="local_dev_secret_key_change_in_production_min_32_chars_long",
        description="Secret key for signing JWT bearer tokens"
    )
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # CORS Configuration
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://labrex.in",
        "https://staging.labrex.in"
    ]

    # AI & Modeling Configuration
    GEMINI_API_KEY: str = Field(default="", description="Google Gemini API key for Copilot")
    FORECAST_HORIZONS: List[int] = [3, 6, 12, 18, 24]
    OPTIMIZATION_TIMEOUT_SECONDS: float = 5.0

    # Rate Limiting
    RATE_LIMIT_DEFAULT_PER_MINUTE: int = 60
    RATE_LIMIT_COPILOT_PER_MINUTE: int = 20
    RATE_LIMIT_OPTIMIZER_PER_MINUTE: int = 15


settings = Settings()
