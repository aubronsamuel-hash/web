from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    app_name: str = Field(default="CoulissesCrew")
    env: str = Field(default="dev")
    log_level: str = Field(default="INFO")
    api_port: int = Field(default=8001)
    request_id_header: str = Field(default="X-Request-ID")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
