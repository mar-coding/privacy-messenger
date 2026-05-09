from pathlib import Path
from typing import Annotated, Any, Literal

from pydantic import AnyUrl, BeforeValidator, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

# Repo root: <repo>/back/app/settings/common.py -> parents[3] = <repo>
_ENV_FILE = Path(__file__).resolve().parents[3] / ".env"


def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)


class CommonSettings(BaseSettings):
    model_config = SettingsConfigDict(
        # Use top level .env file (one level above ./back/)
        # For Docker: environment variables can be loaded by docker-compose from deploy/.env
        # For local dev: environment variables can be loaded from root .env
        env_file=str(_ENV_FILE),
        env_ignore_empty=True,
        extra="ignore",
    )

    # General settings
    PROJECT_NAME: str = "SAM"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: Literal["dev", "staging", "production"] = "dev"
    UNDER_DEVELOPMENT: bool = False  # Set to True for skipping things like OTP, etc
    DEBUG_MODE: bool = False

    # CORS settings
    BACKEND_CORS_ORIGINS: Annotated[list[AnyUrl] | str, BeforeValidator(parse_cors)] = [
        AnyUrl("http://localhost/"),
        AnyUrl("http://localhost:3000/"),
        AnyUrl("http://localhost:8000/"),
        AnyUrl("http://developers.localhost:8000/"),
        AnyUrl("http://api.localhost:8000/"),
        AnyUrl("https://api.localhost:8000/"),
    ]

    @computed_field  # type: ignore[prop-decorator]
    @property
    def all_cors_origins(self) -> list[str]:
        return [
            str(origin).rstrip("/") for origin in self.BACKEND_CORS_ORIGINS
        ]  # + FE_URLS
