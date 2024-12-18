from sqlalchemy.orm import relationship
from .base_model import BaseModel
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import (
    Column,
    JSON,
    ForeignKey,
    String
)


class TableMetadata(BaseModel):
    __tablename__ = 'tables_metadata'
    connection_id = Column(
        UUID(as_uuid=True),
        ForeignKey("db_connections.id", ondelete="CASCADE"),
        default=uuid.uuid4
    )
    json_props = Column(JSON, nullable=False)
    table_name = Column(String, nullable=False)
    schema_name = Column(String, nullable=False)
    comment = Column(String, nullable=True)
    group = Column(String, nullable=True)

    db_connection = relationship(
        "DBConnections" #, back_populates="db_connections"
    )