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
    DbConnectionDeleteOutput,
    ConnectionsOptionValues,
    DbConnectionPartialResponse,
    DbConnectionFullResponse,
    SupportedDbTypes
)
from services.fernet_service import get_fernet

from .utils import wrap_values

from repository.db_settings import (
    get_all_db_connection,
    insert_db_connection,
    get_db_connection,
    update_db_connection,
    delete_db_connection
)

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

tags = ["connections"]


@router.get(
        "/db_connections",
        tags=tags)
async def get_settings(
    option: ConnectionsOptionValues,
    token: Annotated[Token, Depends(oauth2_scheme)],
    db=Depends(get_session)
) -> list[DbConnectionFullResponse] | list[DbConnectionPartialResponse]:

    if option == ConnectionsOptionValues.all:
        check_admin_privs(token)

    return wrap_values(
       await get_all_db_connection(db),
       option
    )


@router.post(
        "/db_connections",
        response_model=DbConnectionResponse,
        tags=tags)
async def save_setting(
    data: DbConnectionInput,
    token: Annotated[Token, Depends(oauth2_scheme)],
    db=Depends(get_session),
    crypt_service=Depends(get_fernet)
):
    check_admin_privs(token)
    return await insert_db_connection(db, data, crypt_service)


@router.get("/db_connections/{connection_id}", tags=tags)
async def get_setting(
    connection_id: UUID,
    token: Annotated[Token, Depends(oauth2_scheme)],
    db=Depends(get_session),
    crypt_service=Depends(get_fernet)
):
    check_admin_privs(token)
    return await get_db_connection(db, connection_id, crypt_service)


@router.patch("/db_connections/{connection_id}", tags=tags)
async def update_setting(
    connection_id: UUID,
    data: DbConnectionUpdateInput,
    token: Annotated[Token, Depends(oauth2_scheme)],
    db=Depends(get_session),
    crypt_service=Depends(get_fernet)
):
    check_admin_privs(token)
    return await update_db_connection(
        db, data, connection_id, crypt_service
    )


@router.delete("/db_connections/{connection_id}", tags=tags)
async def delete_setting(
    connection_id: UUID,
    token: Annotated[Token, Depends(oauth2_scheme)],
    db=Depends(get_session)
) -> DbConnectionDeleteOutput:
    check_admin_privs(token)
    return await delete_db_connection(db, connection_id)


@router.get(
        "/database_types",
        tags=tags)
def get_db_types(
    _: Annotated[Token, Depends(oauth2_scheme)],
) -> list[SupportedDbTypes]:

    return [x.value for x in SupportedDbTypes]
