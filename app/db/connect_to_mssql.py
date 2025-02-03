import pymssql
import os

from app.core.config import get_app_settings

def connect_mssql_init():
    settings = get_app_settings()
    user = settings.ms_user
    pwd = settings.ms_pwd
    host = settings.ms_host
    port = settings.ms_port
    db = settings.ms_db
    return user, pwd, host, port, db

def to_as400_mssql():
    user, pwd, host, port, db = connect_mssql_init()
    conn = pymssql.connect(host=host, user=user, password=pwd, database=db)
    return conn
