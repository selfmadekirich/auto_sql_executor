from fastapi import APIRouter, Depends
from database import get_session
from uuid import UUID
from .managers.sql_generation_managers import SqlGenerationManager
from .models import (
    GenerationInfoOutput,
    GenerationInfoInput,
    GenerationResultOutput
)
from repository.ai_profiles import get_ai_profiles
from services.fernet_service import get_fernet
from routers.ai_profile.models import AIProfileInfoFull
from .providers.llm_service_provider import LLMServiceProvider
from fastapi import HTTPException


router = APIRouter(prefix="/generate")


@router.get(
        "/{connection_id}/info",
        response_model=GenerationInfoOutput,
        tags=["generation"]
)
async def get_generation_info(
    connection_id: UUID,
    user_query: str,
    db=Depends(get_session)
):
    m = SqlGenerationManager(
        db,
        connection_id,
        GenerationInfoInput(user_query=user_query)
    )
    gs = await m.generate_sql()
    prompt = m.prompt
    return GenerationInfoOutput(
        user_query=user_query,
        generated_prompt=prompt,
        generated_sql=gs
    )


@router.post(
        "/{connection_id}/results",
        response_model=GenerationResultOutput,
        tags=["generation"]
)
async def get_generation_result(
    connection_id: UUID,
    d: GenerationInfoInput,
    db=Depends(get_session),
    crypt_service=Depends(get_fernet)
):
    try:

        profile = AIProfileInfoFull.from_orm(await get_ai_profiles(
            db, d.profile_id, crypt_service=crypt_service)
        )

        print(f"profile is: {profile}")
        m = SqlGenerationManager(
            db, connection_id,
            d, LLMServiceProvider(profile),
            crypt_service
        )

        print("SQLGEN MANAGER IS INITIALIZED")
        result = await m.execute_generated_query()

        print("result is generated")

        prompt, gq = m.prompt, m.generated_query

        return GenerationResultOutput(
            info=GenerationInfoOutput(
                user_query=d.user_query,
                generated_prompt=prompt,
                generated_sql=gq
            ).model_dump(),
            result=result
        )
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )
