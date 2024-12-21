from pydantic import BaseModel


class LaminiInput(BaseModel):
    query: str


class LaminiOutput(BaseModel):
    generated: str
