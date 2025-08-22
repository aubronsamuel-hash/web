from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    app_name: str = Field(default="CoulissesCrew")
    env: str = Field(default="dev")
    log_level: str = Field(default="INFO")
    api_port: int = Field(default=8001)
    request_id_header: str = Field(default="X-Request-ID")

    # JWT / Auth
    jwt_secret: str = Field(default="change-me-in-local-env")
    jwt_alg: str = Field(default="HS256")
    jwt_exp_min: int = Field(default=60)

    # Admin dev (no prod)
    admin_email: str = Field(default="admin@example.com")
    admin_password: str = Field(default="admin")

    # DB
    db_dsn: str = Field(default="sqlite:///./local.db")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
