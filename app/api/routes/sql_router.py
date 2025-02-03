import json
from fastapi import HTTPException, APIRouter, Query
import pymssql
from app.api.routes.utils import timeit
from app.db.connect_to_mssql import to_as400_mssql
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
import logging

router = APIRouter()

@router.get("/mssql-get-data")
@timeit
async def mssql_sample():
    conn = to_as400_mssql()
    cursor = conn.cursor()
    cursor.execute("""
                    <your-execute-command>
                """)
    rows = cursor.fetchall()
    result = []
    for row in rows:
        user = {}
        user[row[0]] = [row[1], row[2]]
        result.append(user)

    conn.close()
    
    return JSONResponse(content=result)

