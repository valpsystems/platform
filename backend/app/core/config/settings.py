from __future__ import annotations

import json
import os
from pathlib import Path

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application
    APP_NAME: str = "VALP SYSTEMS"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "VALP SYSTEMS Enterprise Backend API"
    APP_ENV: str = "development"
    APP_DEBUG: bool = True
    APP_PORT: int = 8000
    APP_HOST: str = "0.0.0.0"
    APP_SECRET_KEY: str = "change-this-to-a-secure-random-key"
    APP_URL: str = "http://localhost:8000"

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://postgres:password@localhost:5432/valp_systems"
    DATABASE_ECHO: bool = False
    DATABASE_POOL_SIZE: int = 10
    DATABASE_MAX_OVERFLOW: int = 20

    # Testing
    TEST_DATABASE_URL: str = "sqlite+aiosqlite:///./test.db"

    # CORS
    CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:8000"]

    # Trusted Hosts
    TRUSTED_HOSTS: list[str] = ["localhost", "127.0.0.1"]

    # Logging
    LOG_LEVEL: str = "DEBUG"
    LOG_FORMAT: str = "json"

    # SMTP
    SMTP_HOST: str = ""
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_USE_TLS: bool = True
    SMTP_FROM_EMAIL: str = "noreply@valpsystems.com"
    SMTP_FROM_NAME: str = "VALP SYSTEMS"

    # JWT
    JWT_SECRET_KEY: str = "change-this-to-a-secure-jwt-secret-key"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Password
    PASSWORD_MIN_LENGTH: int = 8
    PASSWORD_REQUIRE_UPPERCASE: bool = True
    PASSWORD_REQUIRE_LOWERCASE: bool = True
    PASSWORD_REQUIRE_DIGIT: bool = True
    PASSWORD_REQUIRE_SPECIAL: bool = False

    # Email Verification
    EMAIL_VERIFICATION_TOKEN_EXPIRE_HOURS: int = 24

    # Password Reset
    PASSWORD_RESET_TOKEN_EXPIRE_HOURS: int = 1

    # Rate Limiting (requests per window)
    RATE_LIMIT_ENABLED: bool = False
    RATE_LIMIT_REQUESTS: int = 10
    RATE_LIMIT_WINDOW_SECONDS: int = 60

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # AWS
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    AWS_REGION: str = "us-east-1"

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, v: str | list) -> list:
        if isinstance(v, list):
            return v
        if isinstance(v, str):
            return json.loads(v)
        return ["http://localhost:3000"]

    @field_validator("TRUSTED_HOSTS", mode="before")
    @classmethod
    def parse_trusted_hosts(cls, v: str | list) -> list:
        if isinstance(v, list):
            return v
        if isinstance(v, str):
            return json.loads(v)
        return ["localhost"]

    @property
    def BASE_DIR(self) -> Path:
        return Path(__file__).resolve().parent.parent.parent.parent

    @property
    def LOGS_DIR(self) -> Path:
        path = self.BASE_DIR / "app" / "logs"
        path.mkdir(parents=True, exist_ok=True)
        return path

    @property
    def EMAIL_TEMPLATES_DIR(self) -> Path:
        return self.BASE_DIR / "app" / "emails" / "templates"

    @property
    def is_production(self) -> bool:
        return self.APP_ENV == "production"

    @property
    def is_development(self) -> bool:
        return self.APP_ENV == "development"

    @property
    def is_testing(self) -> bool:
        return self.APP_ENV == "testing"

    @property
    def database_url_async(self) -> str:
        if self.is_testing:
            return self.TEST_DATABASE_URL
        return self.DATABASE_URL

    @property
    def database_url_sync(self) -> str:
        url = self.TEST_DATABASE_URL if self.is_testing else self.DATABASE_URL
        return url.replace("+asyncpg", "").replace("+aiosqlite", "")


settings = Settings()

if os.getenv("APP_ENV") == "testing":
    settings = Settings(
        _env_file=None,
        APP_ENV="testing",
        APP_DEBUG=False,
        DATABASE_ECHO=False,
    )
