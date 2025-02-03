from typing import Union

from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY
from app.api.return_code import Return_Code
from app.core.log_config import logger


async def http422_error_handler(
    request: Request,
    exc: Union[RequestValidationError, ValidationError],
) -> JSONResponse:

    logger.error(
        f"ValidationError: URL={request.url}, HTTP_STATUS_CODE={HTTP_422_UNPROCESSABLE_ENTITY}, METHOD={request.method}, ERROR={exc}"
    )

    return JSONResponse({"return_code": 205, "message": Return_Code[205]})
