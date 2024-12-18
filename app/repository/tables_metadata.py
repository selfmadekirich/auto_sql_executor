from models.table_metadata import TableMetadata
from sqlalchemy.ext.asyncio import AsyncSession
from routers.admin.models import DbConnectionInput
from uuid import UUID


async def get_all_metadata(db: AsyncSession, connection_id: UUID):
    return await TableMetadata.list(
        db, filters={"connection_id": connection_id}
    )


async def get_metadata(
    db: AsyncSession,
    connection_id: UUID,
    id: UUID
):
    return await TableMetadata.get_one(
        db, filters={
            "id": id,
            "connection_id": connection_id
        }
    )


async def insert_metadata(
    db: AsyncSession,
    data: DbConnectionInput
):
    return await TableMetadata.insert(
        db, **data.model_dump()
    )


async def update_metadata(
        db: AsyncSession,
        data: DbConnectionInput,
        id: UUID
):
    return await TableMetadata.update(
        db, filters={
            "id": id
        },
        **data.model_dump()
    )


async def delete_metadata(
        db: AsyncSession,
        id: UUID
):
    return await TableMetadata.delete(
        db, filters={
            "id": id
        }
    )