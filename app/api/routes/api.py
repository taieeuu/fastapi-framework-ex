from fastapi import APIRouter
from app.api.routes import sample_router
from app.api.routes import sql_router

router = APIRouter()
router.include_router(sample_router.router, prefix="/sample_router", tags=["sample_api"])
router.include_router(sql_router.router, prefix="/sql_router", tags=["as400"])