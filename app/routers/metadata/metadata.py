from fastapi import APIRouter, Depends
from database import get_session
from uuid import UUID
from .models import (
    TableMetadataDeleteOutput,
    TableMetadataInput,
    TableMetadataUpdateInput,
    TableMetadataResponse
)
from repository.tables_metadata import (
    get_all_metadata,
    get_metadata,
    delete_metadata,
    update_metadata,
    insert_metadata
)

router = APIRouter(prefix="/db_connections")


@router.get(
        "/{connection_id}/metadata",
        response_model=list[TableMetadataResponse],
        tags=["metadata"])
async def get_connection_metadata(connection_id, db=Depends(get_session)):
    return await get_all_metadata(db, connection_id)


@router.post(
        "/{connection_id}/metadata",
        response_model=TableMetadataResponse,
        tags=["metadata"])
async def save_metadata(
    connection_id: UUID,
    data: TableMetadataInput,
    db=Depends(get_session)
):
    data.connection_id = connection_id
    return await insert_metadata(db, data)


@router.get(
        "/{connection_id}/metadata/{metadata_id}",
        tags=["metadata"])
async def get_setting(
    connection_id: UUID,
    metadata_id: UUID,
    db=Depends(get_session)
):
    return await get_metadata(db, connection_id, metadata_id)


@router.patch("/{connection_id}/metadata/{metadata_id}", tags=["metadata"])
async def update_setting(
    connection_id: UUID,
    metadata_id: UUID,
    data: TableMetadataUpdateInput,
    db=Depends(get_session)
):
    return await update_metadata(
        db, data, metadata_id
    )


@router.delete("/{connection_id}/metadata/{metadata_id}", tags=["metadata"])
async def delete_setting(
    connection_id: UUID,
    metadata_id: UUID,
    db=Depends(get_session)
) -> TableMetadataDeleteOutput:
    return await delete_metadata(db, metadata_id)
