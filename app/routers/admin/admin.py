from typing import Annotated
from fastapi import APIRouter, Depends
from database import get_session
from uuid import UUID
from fastapi.security import OAuth2PasswordBearer
from routers.auth.models import Token
from routers.auth.utils import check_admin_privs
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

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


@router.get(
        "/db_connections/",
        response_model=list[DbConnectionResponse],
        tags=["admin"])
async def get_settings(
    token: Annotated[Token, Depends(oauth2_scheme)],
    db=Depends(get_session)
):
    check_admin_privs(token)
    return await get_all_db_connection(db)


@router.post(
        "/db_connections",
        response_model=DbConnectionResponse,
        tags=["admin"])
async def save_setting(
    data: DbConnectionInput,
    token: Annotated[Token, Depends(oauth2_scheme)],
    db=Depends(get_session)
):
    check_admin_privs(token)
    return await insert_db_connection(db, data)


@router.get("/db_connections/{connection_id}", tags=["admin"])
async def get_setting(
    connection_id: UUID,
    token: Annotated[Token, Depends(oauth2_scheme)],
    db=Depends(get_session)
):
    check_admin_privs(token)
    return await get_db_connection(db, connection_id)


@router.patch("/db_connections/{connection_id}", tags=["admin"])
async def update_setting(
    connection_id: UUID,
    data: DbConnectionUpdateInput,
    token: Annotated[Token, Depends(oauth2_scheme)],
    db=Depends(get_session)
):
    check_admin_privs(token)
    return await update_db_connection(
        db, data, connection_id
    )


@router.delete("/db_connections/{connection_id}", tags=["admin"])
async def delete_setting(
    connection_id: UUID,
    token: Annotated[Token, Depends(oauth2_scheme)],
    db=Depends(get_session)
) -> DbConnectionDeleteOutput:
    check_admin_privs(token)
    return await delete_db_connection(db, connection_id)
