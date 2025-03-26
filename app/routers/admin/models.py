from pydantic import BaseModel, ConfigDict
from enum import Enum
import uuid


class ConnectionsOptionValues(str, Enum):
    all = "All"
    partly = "Partial"


class SupportedDbTypes(str, Enum):
    Postgres = "postgres"
    MySQL = "mysql"


class ConnectionInfo(BaseModel):
    host: str
    port: int
    user: str
    password: str
    db_name: str
    schema_name: str
    description: str
    name: str


class ConnectionInfoPartial(BaseModel):
    name: str
    description: str


class DbConnectionPartialResponse(BaseModel):
    id: uuid.UUID
    db_type: str
    json_props: ConnectionInfoPartial

    model_config = ConfigDict(from_attributes=True)


class DbConnectionResponse(BaseModel):
    id: uuid.UUID
    db_type: str
    json_props: dict

    model_config = ConfigDict(from_attributes=True)


class DbConnectionInput(BaseModel):
    db_type: SupportedDbTypes
    json_props: ConnectionInfo

    model_config = ConfigDict(from_attributes=True)


class DbConnectionDeleteOutput(BaseModel):
    id: uuid.UUID
    model_config = ConfigDict(from_attributes=True)


class DbConnectionUpdateInput(BaseModel):
    db_type: SupportedDbTypes
    json_props: ConnectionInfo
