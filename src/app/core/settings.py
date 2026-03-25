from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    app_name: str = "Vodle API"
    app_version: str = "1.0.0"

    secret_key: str = Field(
        default="your_secret_key",
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

    database_url: str = Field(
        default="sqlite:///./vodle.db",
        description="Database connection URL",
    )


settings = Settings()
