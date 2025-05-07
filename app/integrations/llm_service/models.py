from typing import Optional
from pydantic import BaseModel


class LaminiInput(BaseModel):
    query: str
    prompt: str


class OpenRouterInput(BaseModel):
    model_name: str
    API_KEY: str
    prompt: str


class BasicOutput(BaseModel):
    generated: Optional[str]
