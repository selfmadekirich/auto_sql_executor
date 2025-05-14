from fastapi import APIRouter, Depends
from database import get_session
from uuid import UUID
from .managers.sql_generation_managers import SqlGenerationManager
from .models import (
    GenerationInfoOutput,
    GenerationInfoInput,
    GenerationResultOutput,
    ResultsLoadInfoInput,
    ResultsLoadResponse
)
from routers.meta_extraction.managers.meta_extractor_manager import (
    MetaExtractorManager
)
from repository.ai_profiles import get_ai_profiles
from repository.db_settings import get_db_connection
from services.fernet_service import get_fernet
from routers.ai_profile.models import AIProfileInfoFull
from .providers.llm_service_provider import LLMServiceProvider
from fastapi import HTTPException
from loguru import logger


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

        logger.info(f"profile is: {profile}")
        m = SqlGenerationManager(
            db, connection_id,
            d, LLMServiceProvider(profile),
            crypt_service
        )

        result = await m.execute_generated_query()

        logger.info("result is generated")

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
        logger.exception(str(e))
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )


@router.post(
        "/{connection_id}/results/load",
        response_model=ResultsLoadResponse,
        tags=["generation"]
)
async def get_generation_result_parts(
    connection_id: UUID,
    d: ResultsLoadInfoInput,
    db=Depends(get_session),
    crypt_service=Depends(get_fernet)
):
    try:

        logger.info("start /results/load")
        conn = await get_db_connection(
            db,
            connection_id,
            crypt_service
        )

        m = MetaExtractorManager(conn, reflect=False)

        result = m.execute_sql(d.sql_query, page=d.page)

        return ResultsLoadResponse(
            sql_query=d.sql_query,
            page=d.page,
            size=len(result),
            results=result
        )
    except Exception as e:
        logger.exception(str(e))
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )
