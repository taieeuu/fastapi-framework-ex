import logging

from pydantic import ConfigDict
from app.core.settings.app import AppSettings


class DevAppSettings(AppSettings):
    debug: bool = True

    title: str = "Dev FastAPI application"

    logging_level: int = logging.DEBUG

    host_name: str = "localhost"

    model_config = ConfigDict(
        env_file=".env"
    )
