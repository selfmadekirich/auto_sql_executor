from pydantic import BaseModel
from models.db_connections import DBConnections
from ..metadata.models import TableMetadataInput, TableProps
from uuid import UUID

class MetaExtractorConfig(BaseModel):
    host: str
    port: str
    user: str
    db_name: str
    passw: str
    schema_name: str
    connection_id: UUID

    @staticmethod
    def from_db_connections(db: DBConnections):
        return MetaExtractorConfig(
            host=db.json_props.get("host"),
            port=str(db.json_props.get("port")),
            user=db.json_props.get("user"),
            passw=db.json_props.get("password"),
            db_name=db.json_props.get("db_name"),
            schema_name=db.json_props.get("schema_name", "public"),
            connection_id=db.id
        )


class ExtractorMetaTable(BaseModel):
    table_name: str
    schema_name: str
    comment: str | None
    connection_id: UUID
    json_props: dict

    def to_table_metadata_input(self) -> TableMetadataInput:
        return TableMetadataInput(
            table_name=self.table_name,
            schema_name=self.schema_name,
            connection_id=self.connection_id,
            comment=self.comment,
            group=None,
            json_props=TableProps(
                columns=self.json_props.get("columns"),
                refs=[]
            )
        )


class OkResponse(BaseModel):
    status: str = "ok"
