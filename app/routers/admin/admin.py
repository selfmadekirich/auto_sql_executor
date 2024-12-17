from fastapi import APIRouter, Depends
from database import get_session
from uuid import UUID
from .models import (
    DbConnectionInput,
    DbConnectionResponse,
    DbConnectionUpdateInput,
    DbConnectionDeleteOutput
)
from repository.db_settings import (
    get_all_db_connection,
    insert_db_connection,
    get_db_connection,
    update_db_connection,
    delete_db_connection
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
async def get_setting(connection_id: UUID, db=Depends(get_session)):
    return await get_db_connection(db, connection_id)


@router.post("/db_connections/{connection_id}", tags=["admin"])
async def update_setting(
    connection_id: UUID, 
    data: DbConnectionUpdateInput,
    db=Depends(get_session)
):
    return await update_db_connection(
        db, data, connection_id
    )


@router.delete("/db_connections/{connection_id}", tags=["admin"])
async def delete_setting(
    connection_id: UUID,
    db=Depends(get_session)
) -> DbConnectionDeleteOutput:
    return await delete_db_connection(db, connection_id)
