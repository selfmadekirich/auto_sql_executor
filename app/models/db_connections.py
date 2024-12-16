from .base_model import BaseModel
from sqlalchemy import (
    Column,
    JSON,
    String
)


class DBConnections(BaseModel):
    __tablename__ = 'db_connections'
    db_type = Column(String, nullable=False)
    json_props = Column(JSON, nullable=False)
