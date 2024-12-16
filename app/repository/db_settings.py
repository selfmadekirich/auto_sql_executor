from models.db_connections import DBConnections
from sqlalchemy.ext.asyncio import AsyncSession
from routers.admin.models import DbConnectionInput


async def get_all_db_connection(db: AsyncSession):
    return await DBConnections.list(db)


async def insert_db_connection(
        db: AsyncSession,
        data: DbConnectionInput):
    return await DBConnections.insert(
        db, **data.model_dump()
    )
