from mongoengine import connect
from pymongo import MongoClient
import os

from app.core.config import get_app_settings


def connect_init():
    settings = get_app_settings()
    user = settings.mongo_user
    pwd = settings.mongo_pwd
    host = settings.mongo_host
    port = settings.mongo_port
    db = settings.mongo_db
    return user, pwd, host, port, db

def to_mdc_prod():
    user, pwd, host, port, db = connect_init()
    connect(
        db = {db},
        username = {user},
        password = {pwd},
        host = f'mongodb://{user}:{pwd}@{host}:{port}/?authSource={db}'
    )

def connect_with_pymongo():
    user, pwd, host, port, db = connect_init()
    return MongoClient(f'mongodb://{user}:{pwd}@{host}:{port}/?authSource={db}')
