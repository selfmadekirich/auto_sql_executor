from models.db_connections import DBConnections
from sqlalchemy.ext.asyncio import AsyncSession
from routers.admin.models import DbConnectionInput
from uuid import UUID


async def get_all_db_connection(db: AsyncSession):
    return await DBConnections.list(db)


async def get_db_connection(
    db: AsyncSession,
    id: UUID
):
    return await DBConnections.get_one(
        db, filters={
            "id": id
        }
    )


async def insert_db_connection(
    db: AsyncSession,
    data: DbConnectionInput
):
    return await DBConnections.insert(
        db, **data.model_dump()
    )


async def update_db_connection(
        db: AsyncSession,
        data: DbConnectionInput,
        id: UUID
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