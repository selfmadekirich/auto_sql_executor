from .base_model import BaseModel
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import (
    Column,
    String
)


class AIProfile(BaseModel):
    __tablename__ = 'ai_profiles'
    profile_name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    service = Column(String, nullable=False)
    model_name = Column(String, nullable=False)
    auth_token = Column(String, nullable=False)
