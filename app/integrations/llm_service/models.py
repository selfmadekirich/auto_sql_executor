from pydantic import BaseModel


class LaminiInput(BaseModel):
    query: str
    prompt: str


class LaminiOutput(BaseModel):
    generated: str
