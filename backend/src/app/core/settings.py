from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
DB_PATH = BASE_DIR / "data" / "vodle.db"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    app_name: str = "Vodle API"
    app_version: str = "1.0.0"

    secret_key: str = Field(
        default="fallback-dev-secret-change-me",
        description="The secret key for JWT",
    )

    algorithm: str = Field(
        default="HS256",
        description="The algorithm used for JWT",
    )

    access_token_expire_minutes: int = Field(
        default=30,
        description="Access token expiration time in minutes",
    )

    cookie_secure: bool = Field(
        default=False,
        description="Whether auth cookies should require HTTPS",
    )

    app_timezone: str = Field(
        default="America/Los_Angeles",
        description="Timezone used to choose the active daily question",
    )

    auto_seed_daily_questions: bool = Field(
        default=True,
        description="Whether startup should schedule missing daily questions",
    )

    scheduled_question_days: int = Field(
        default=30,
        description="How many days of daily questions to keep scheduled",
    )

    archived_question_days: int = Field(
        default=30,
        description="How many past days of daily questions to keep scheduled",
    )

    database_url: str = Field(
        default=f"sqlite:///{DB_PATH.as_posix()}",
        description="Database connection URL",
    )


settings = Settings()
