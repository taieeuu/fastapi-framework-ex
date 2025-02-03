from enum import Enum
from pydantic import ConfigDict, Field
from pydantic_settings import BaseSettings

class AppEnvTypes(Enum):
    prod: str = "prod"
    uat: str = "uat"
    dev: str = "dev"

class RedisSettings(BaseSettings):
    redis_host: str = Field(..., json_schema_extra={"env": "REDIS_HOST"})
    redis_port: str = Field(..., json_schema_extra={"env": "REDIS_PORT"})
    redis_pwd: str = Field(..., json_schema_extra={"env": "REDIS_PWD"})
    redis_db: str = Field(..., json_schema_extra={"env": "REDIS_DB"})

class MongodbSettings(BaseSettings):
    mongo_host: str = Field(..., json_schema_extra={"env": "MONGO_HOST"})
    mongo_db: str = Field(..., json_schema_extra={"env": "MONGO_DB"})
    mongo_user: str = Field(..., json_schema_extra={"env": "MONGO_USER"})
    mongo_pwd: str = Field(..., json_schema_extra={"env": "MONGO_PWD"})
    mongo_port: str = Field(..., json_schema_extra={"env": "MONGO_PORT"})

class EnvSettings(BaseSettings):
    app_env: str = Field(..., json_schema_extra={"env": "APP_ENV"})

class MsSqlSettings(BaseSettings):
    ms_host: str = Field(..., json_schema_extra={"env": "MS_HOST"})
    ms_db: str = Field(..., json_schema_extra={"env": "MS_DB"})
    ms_user: str = Field(..., json_schema_extra={"env": "MS_USER"})
    ms_pwd: str = Field(..., json_schema_extra={"env": "MS_PWD"})
    ms_port: str = Field(..., json_schema_extra={"env": "MS_PORT"})

class ODBCSettings(BaseSettings):
    odbc_sys: str = Field(..., json_schema_extra={"env": "ODBC_SYS"})
    odbc_uid: str = Field(..., json_schema_extra={"env": "ODBC_UID"})
    odbc_pwd: str = Field(..., json_schema_extra={"env": "ODBC_PWD"})

class BaseAppSettings(
    RedisSettings, MongodbSettings, EnvSettings, MsSqlSettings, ODBCSettings
):
    model_config = ConfigDict(
        env_file=".env"
    )
