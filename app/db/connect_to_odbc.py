from app.core.config import get_app_settings
import pyodbc


def connect_init():
    settings = get_app_settings()
    odbc_back_sys = settings.odbc_sys
    odbc_back_uid = settings.odbc_uid
    odbc_back_pwd = settings.odbc_pwd

    return odbc_back_sys, odbc_back_uid, odbc_back_pwd


def to_odbc():
    try:
        odbc_back_sys, odbc_back_uid, odbc_back_pwd = connect_init()
        conn = pyodbc.connect(
            f"DRIVER=IBM i Access ODBC Driver;SYSTEM={odbc_back_sys};UID={odbc_back_uid};PWD={odbc_back_pwd}"
        )
    except Exception:
        return None
    return conn
