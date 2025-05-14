import uuid
from pydantic import BaseModel


class GenerationInfoInput(BaseModel):
    user_query: str
    profile_id: uuid.UUID


class ResultsLoadInfoInput(BaseModel):
    sql_query: str
    page: int
    size: int


class ResultsLoadResponse(BaseModel):
    sql_query: str
    page: int
    size: int
    results: list[dict]


class GenerationInfoOutput(BaseModel):
    user_query: str
    generated_prompt: str
    generated_sql: str


class GenerationResultOutput(BaseModel):
    info: GenerationInfoOutput
    result: list[dict]
