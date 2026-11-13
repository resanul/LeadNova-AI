from typing import List, Union
from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "GlobalLead AI"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ]

    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./globallead.db"

    # Security
    SECRET_KEY: str = "production-grade-random-secret-key-change-in-production-leadnova-ai"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440

    # Initial Super Admin
    FIRST_SUPERUSER_EMAIL: str = "admin@globallead.ai"
    FIRST_SUPERUSER_PASSWORD: str = "AdminPassword123!"

    # Telephony
    TWILIO_ACCOUNT_SID: str = "AC_mock_twilio_account_sid"
    TWILIO_AUTH_TOKEN: str = "mock_twilio_auth_token"
    DEFAULT_CALL_TIMEOUT_SECONDS: int = 60

    # AI Provider (Google Antigravity Engine)
    AI_PROVIDER: str = "antigravity"
    AI_MODEL_NAME: str = "gemini-3.8-flash"
    GEMINI_API_KEY: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )


settings = Settings()
