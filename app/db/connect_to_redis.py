import redis
import os

from app.core.config import get_app_settings

def get_redis_client():
    settings = get_app_settings()
    client = redis.StrictRedis(
        host = settings.redis_host,
        port = settings.redis_port,
        password = settings.redis_pwd,
        db = settings.redis_db,
        decode_responses = True 
    )
    return client
