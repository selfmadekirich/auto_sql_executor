from pydantic import BaseModel, ConfigDict
import uuid
from typing import Optional


class ColumnProps(BaseModel):
    name: str
    type: str
    nullable: bool
    comment: str | None


class RefProps(BaseModel):
    table_name: str
    column_name: str


class TableProps(BaseModel):
    columns: list[ColumnProps]
    refs: Optional[list[RefProps]]


class TableMetadataResponse(BaseModel):
    id: uuid.UUID
    json_props: dict
    table_name: str
    schema_name: str
    connection_id: uuid.UUID
    comment: str | None
    group: str | None

    model_config = ConfigDict(from_attributes=True)


class TableMetadataInput(BaseModel):
    table_name: str
    schema_name: str
    comment: str | None
    connection_id: uuid.UUID
    group: str | None
    json_props: TableProps

    model_config = ConfigDict(from_attributes=True)


class TableMetadataDeleteOutput(BaseModel):
    id: uuid.UUID
    model_config = ConfigDict(from_attributes=True)


class TableMetadataUpdateInput(BaseModel):
    table_name: str
    schema_name: str
    comment: str
    group: str
    json_props: TableProps
