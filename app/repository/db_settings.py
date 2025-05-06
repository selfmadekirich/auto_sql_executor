from models.db_connections import DBConnections
from sqlalchemy.ext.asyncio import AsyncSession
from routers.admin.models import DbConnectionInput
from services.fernet_service import FernetService
from uuid import UUID
from utils.decorators import proccess_password


async def get_all_db_connection(db: AsyncSession):
    return await DBConnections.list(db)


@proccess_password(
        crypt=False
)
async def get_db_connection(
    db: AsyncSession,
    id: UUID,
    crypt_service: FernetService = None
):
    res = await DBConnections.get_one(
        db, filters={
            "id": id
        }
    )

    return res


@proccess_password(
        crypt=True
)
async def insert_db_connection(
    db: AsyncSession,
    data: DbConnectionInput,
    crypt_service: FernetService
):
    return await DBConnections.insert(
        db, **data.model_dump()
    )


@proccess_password(
        crypt=True
)
async def update_db_connection(
        db: AsyncSession,
        data: DbConnectionInput,
        id: UUID,
        crypt_service: FernetService
):
    return await DBConnections.update(
        db, filters={
            "id": id
        },
        **data.model_dump()
    )


async def delete_db_connection(
        db: AsyncSession,
        id: UUID
):
    return await DBConnections.delete(
        db, filters={
            "id": id
        }
    )