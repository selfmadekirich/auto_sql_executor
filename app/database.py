from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker
)
from settings import get_settings


DATABASE_URL = get_settings().DATABASE_URI

engine = create_async_engine(DATABASE_URL, echo=True, future=True)

async_session = async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
)


async def get_session() -> AsyncSession:
    try:
        async with async_session() as session:
            yield session
    except Exception as e:
        print(e)