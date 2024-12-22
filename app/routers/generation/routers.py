from fastapi import APIRouter, Depends
from database import get_session
from uuid import UUID
from .managers.sql_generation_managers import SqlGenerationManager
from .models import (
    GenerationInfoOutput,
    GenerationInfoInput,
    GenerationResultOutput
)

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
    db=Depends(get_session)
):
    m = SqlGenerationManager(
        db,
        connection_id,
        d
    )
    result = await m.execute_generated_query()
    prompt, gq = m.prompt, m.generated_query
    return GenerationResultOutput(
        info=GenerationInfoOutput(
            user_query=d.user_query,
            generated_prompt=prompt,
            generated_sql=gq
        ).model_dump(),
        result=result
    )
