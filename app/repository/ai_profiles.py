from models.ai_profile import AIProfile
from sqlalchemy.ext.asyncio import AsyncSession
from routers.ai_profile.models import AIProfileInput
from services.fernet_service import FernetService
from uuid import UUID
from utils.decorators import proccess_tokens, check_logic
from routers.ai_profile.exceptions import UnsupportedAIModel
from routers.ai_profile.utils import check_model_is_supported

async def get_all_ai_profiles(db: AsyncSession):
    return await AIProfile.list(db)


@proccess_tokens(
        crypt=False
)
async def get_ai_profiles(
    db: AsyncSession,
    id: UUID,
    crypt_service: FernetService = None
):
    res = await AIProfile.get_one(
        db, filters={
            "id": id
        }
    )

    return res


@proccess_tokens(
        crypt=True
)
@check_logic(
        check_function=check_model_is_supported,
        exception=UnsupportedAIModel
)
async def insert_ai_profiles(
    db: AsyncSession,
    data: AIProfileInput,
    crypt_service: FernetService
):
    return await AIProfile.insert(
        db, **data.model_dump()
    )


@check_logic(
        check_function=check_model_is_supported,
        exception=UnsupportedAIModel
)
@proccess_tokens(
        crypt=True
)
async def update_ai_profiles(
        db: AsyncSession,
        data: AIProfileInput,
        id: UUID,
        crypt_service: FernetService
):
    return await AIProfile.update(
        db, filters={
            "id": id
        },
        **data.model_dump()
    )


async def delete_ai_profiles(
        db: AsyncSession,
        id: UUID
):
    return await AIProfile.delete(
        db, filters={
            "id": id
        }
    )
