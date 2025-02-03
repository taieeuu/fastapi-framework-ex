from fastapi import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse
from app.api.return_code import Return_Code
from app.core.log_config import logger
import logging


async def http_error_handler(request: Request, exc: HTTPException) -> JSONResponse:

    logging.error(f'HTTPException: URL={request.url}, HTTP_STATUS_CODE={exc.status_code}, METHOD={request.method}, ERROR: {exc}')

    logger.error(f'HTTPException: URL={request.url}, HTTP_STATUS_CODE={exc.status_code}, METHOD={request.method}, ERROR: {exc}')

    if exc.status_code==404:

        return JSONResponse({"return_code": 401, "message": Return_Code[401]})


    return JSONResponse({"return_code": 400, "message": Return_Code[400]})
