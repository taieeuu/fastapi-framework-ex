from fastapi import status
from starlette.requests import Request
from starlette.responses import JSONResponse
from app.api.return_code import Return_Code
from app.core.log_config import logger
import logging


async def value_error_handler(request: Request, exc: ValueError) -> JSONResponse:

    error_message = str(exc).lower()
    status_code = 0
    if "unconverted data" in error_message:
        status_code = 400  # 日期格式錯誤等用戶輸入問題
    elif "unprocessable" in error_message:
        status_code = 422  # 資料驗證失敗
    elif "internal" in error_message:
        status_code = 500  # 伺服器邏輯問題

    logging.error(f"ValueError occurred: URL={request.url}, METHOD={request.method}, ERROR={exc}")

    logger.error(f"ValueError occurred: URL={request.url}, HTTP_STATUS_CODE={status_code}, METHOD={request.method}, ERROR={exc}")

    return JSONResponse({"return_code": 300, "message": Return_Code[300]})
