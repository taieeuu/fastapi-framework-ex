from fastapi import FastAPI, HTTPException, Request, APIRouter, Query
from fastapi.responses import JSONResponse, HTMLResponse
from app.core.config import get_app_settings
from app.db.connect_to_mdc import connect_with_pymongo
from app.api.func.sample_api_func import *
from app.core.api_config import *
from app.api.routes.utils import *
from app.db.connect_to_redis import get_redis_client
import plotly.io as pio
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import pandas as pd
from app.core.log_config import logger
import logging
from app.models.example_model import ExampleRequest

router = APIRouter()
redis_client = get_redis_client()

@router.get("/whose_api")
@timeit
async def whose_api(
    code: str = Query(..., description="code"),
):
    response = {code: f"code_{code}"}

    redis_cache = redis_client.get(code)

    if redis_cache:
        return JSONResponse(content=json.loads(redis_cache))

    store_response_in_redis(code, response, redis_client)

    return response

@router.get("/debug/http_error")
async def http_error_test():
    raise HTTPException(status_code=400, detail="This is test error message")

@router.get("/debug/value_error")
async def value_error_test():
    raise ValueError("This is test error message")

@router.delete("/debug/cache_clear", tags=["sample_api"])
async def clear_cache(request: ExampleRequest):
    try:
        code = request.code
        cache_key = f"{code}"
        redis_client.delete(cache_key)
        print(f'Cache for key {cache_key} cleared')
        return JSONResponse(content="Cache cleared", status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
@router.get("/debug/test")
async def test():
    
    logging.debug('test logging')

    logger.error('test logging')
    return 0

@router.get("/debug/settings")
def get_settings():
    settings = get_app_settings()
    return {
        "app_env": settings.app_env,
        "mongo_host": settings.mongo_host,
        "mongo_db": settings.mongo_db,
        "mongo_user": settings.mongo_user,
        "mongo_pwd": settings.mongo_pwd,
        "mongo_port": settings.mongo_port,
        "redis_host": settings.redis_host,
        "redis_port": settings.redis_port,
        "redis_pwd": settings.redis_pwd,
        "redis_db": settings.redis_db
    }
