from pydantic import BaseModel


class LlamaInput(BaseModel):
    query: str
    prompt: str


class LlamaOutput(BaseModel):
    generated: str
