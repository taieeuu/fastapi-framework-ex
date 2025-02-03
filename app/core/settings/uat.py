import logging
from typing import List
from app.core.settings.app import AppSettings


class UatAppSettings(AppSettings):
    debug: bool = False

    title: str = "Uat FastAPI application"

    # secret_key: SecretStr = SecretStr("uat_secret")

    allowed_hosts: List[str] = ["*"]

    logging_level: int = logging.DEBUG

    host_name: str = "<uat_ip_name>"
