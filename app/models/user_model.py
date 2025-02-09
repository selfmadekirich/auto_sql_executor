from .base_model import BaseModel
from sqlalchemy import (
    Column,
    String
)


class User(BaseModel):
    __tablename__ = 'users'
    username = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    scopes = Column(String, nullable=True)
