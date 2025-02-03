from app.core.settings.app import AppSettings
from typing import List
from pydantic import ConfigDict


class ProdAppSettings(AppSettings):
    allowed_hosts: List[str] = ["*"]

    host_name: str = "<prod_ip_name>"

    model_config = ConfigDict(env_file=".env")
