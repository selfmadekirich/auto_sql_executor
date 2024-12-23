from models.user_model import User
from sqlalchemy.ext.asyncio import AsyncSession
from routers.auth.models import UserSingUp
from uuid import UUID


async def get_user(db: AsyncSession, username: str):
    return await User.get_one(
        db, filters={"username": username}
    )


async def save_user(db: AsyncSession, data: UserSingUp):
    return await User.insert(
        db, **data.model_dump()
    )

