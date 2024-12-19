from pydantic import BaseModel
from models.db_connections import DBConnections


class MetaExtractorConfig(BaseModel):
    host: str
    port: str
    user: str
    db_name: str
    passw: str

    @staticmethod
    def from_db_connections(db: DBConnections):
        return MetaExtractorConfig(
            host=db.json_props.get("host"),
            port=str(db.json_props.get("port")),
            user=db.json_props.get("user"),
            passw=db.json_props.get("password"),
            db_name=db.json_props.get("db_name")
        )


class OkResponse(BaseModel):
    status: str = "ok"
