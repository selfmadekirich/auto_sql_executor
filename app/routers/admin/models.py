from pydantic import BaseModel, ConfigDict
import uuid


class DbConnectionResponse(BaseModel):
    id: uuid.UUID
    db_type: str
    json_props: dict

    model_config = ConfigDict(from_attributes=True)


class DbConnectionInput(BaseModel):
    db_type: str
    json_props: dict

    model_config = ConfigDict(from_attributes=True)
