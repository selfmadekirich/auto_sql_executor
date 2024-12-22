from fastapi import APIRouter, Depends
from .models import OkResponse
from database import get_session
from repository.db_settings import get_db_connection
from repository.tables_metadata import (
    insert_all_metadata,
    delete_all_metadata
)
from .managers.meta_extractor_manager import MetaExtractorManager


router = APIRouter()


@router.post(
        "/extract_meta/{connection_id}",
        response_model=OkResponse,
        tags=["meta extraction"]
)
async def extract_metadata(connection_id, db=Depends(get_session)):
    conn = await get_db_connection(db, connection_id)
    m = MetaExtractorManager(conn)
    await delete_all_metadata(db, connection_id)
    data = m.extract()
    await insert_all_metadata(
        db,
        data
    )
    return OkResponse()
