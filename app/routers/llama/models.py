from pydantic import BaseModel


class LlamaInput(BaseModel):
    query: str
    prompt: str
    model_config = {
        "json_schema_extra": {
            "examples": [
              {
                "query": "list all users",
                "prompt": """You generate PostgreSQL only.
Using provided schema: create table users ( name text);
generate SQL to user request"""
              }
            ]
        }
    }


class LlamaOutput(BaseModel):
    generated: str
