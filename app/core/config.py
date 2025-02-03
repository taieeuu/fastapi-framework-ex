# app.py
from functools import lru_cache
from typing import Dict, Type
from app.core.settings.production import ProdAppSettings
from app.core.settings.development import DevAppSettings
from app.core.settings.uat import UatAppSettings
from app.core.settings.base import BaseAppSettings
from app.core.settings.app import AppSettings

environments: Dict[str, Type[AppSettings]] = {
    "dev": DevAppSettings,
    "prod": ProdAppSettings,
    "uat": UatAppSettings,
}

@lru_cache
def get_app_settings() -> AppSettings:
    app_env = BaseAppSettings().app_env
    config = environments[app_env]
    return config()
