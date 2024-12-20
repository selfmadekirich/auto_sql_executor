from fastapi import APIRouter, Depends
from routers.meta_extraction.managers.meta_extractor_manager import (
    MetaExtractorManager
)
from database import get_session
from uuid import UUID
from .models import (
    GenerationInfoOutput,
    GenerationInfoInput,
    GenerationResultOutput
)

from routers.metadata.models import TableMetadataResponse

from .promt_generation.full_ddl_prompt_generator import (
    FullDDLPromptGenerator
)

from repository.tables_metadata import (
    get_all_metadata
)
from repository.db_settings import (
    get_db_connection
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
    generator = FullDDLPromptGenerator()
    data = await get_all_metadata(db, connection_id)
    prompt = generator.generate_prompt(
        user_query=user_query,
        tables_info=[TableMetadataResponse.from_orm(x) for x in data]
    )
    return GenerationInfoOutput(
        user_query=user_query,
        generated_prompt=prompt,
        generated_sql="select * from dual;"
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
    #generator = FullDDLPromptGenerator()
    #data = await get_all_metadata(db, connection_id)
    #prompt = generator.generate_prompt(
    #    user_query=user_query,
    #    tables_info=[TableMetadataResponse.from_orm(x) for x in data]
    #)
    conn = await get_db_connection(db, connection_id)
    m = MetaExtractorManager(conn)
    return GenerationResultOutput(
        info=GenerationInfoOutput(
            user_query=d.user_query,
            generated_prompt="aaaaa",
            generated_sql="select * from dual;"
        ).model_dump(),
        result=m.execute_sql("select * from video_games.genre;")
    )
