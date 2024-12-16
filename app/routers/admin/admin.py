from fastapi import APIRouter, Depends
from database import get_session
from .models import (
    DbConnectionInput,
    DbConnectionResponse
)
from repository.db_settings import (
    get_all_db_connection,
    insert_db_connection
)

router = APIRouter()


@router.get(
        "/db_connections/",
        response_model=list[DbConnectionResponse],
        tags=["admin"])
async def get_settings(db=Depends(get_session)):
    return await get_all_db_connection(db)


@router.post(
        "/db_connections",
        response_model=DbConnectionResponse,
        tags=["admin"])
async def save_setting(data: DbConnectionInput, db=Depends(get_session)):
    return await insert_db_connection(db, data)


@router.get("/db_connections/{connection_id}", tags=["admin"])
async def get_setting(connection_id: str):
    return [{"username": "Rick"}, {"username": "Morty"}]


@router.post("/db_connections/{connection_id}", tags=["admin"])
async def update_setting():
    return [{"username": "Rick"}, {"username": "Morty"}]


@router.delete("/db_connections/{connection_id}", tags=["admin"])
async def delete_setting():
    return [{"username": "Rick"}, {"username": "Morty"}]
