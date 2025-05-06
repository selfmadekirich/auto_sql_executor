from pydantic import BaseModel, ConfigDict
from enum import Enum
import uuid


class AIProfilesOptionValues(str, Enum):
    all = "All"
    partly = "Partial"


class SupportedServices(str, Enum):
    Groq = "Groq"
    OpenRouter = "OpenRouter"
    Custom = "Custom"


class SupportedModels(list, Enum):
    Groq = ["llama-3.3-70b-versatile", "qwen-2.5-coder-32b"]
    OpenRouter = [""]
    Custom = [""]


class AIProfileInfo(BaseModel):
    profile_name: str
    description: str
    service: str
    model_name: str


class AIProfileInfoFull(BaseModel):
    profile_name: str
    description: str
    service: str
    model_name: str
    auth_token: str


class AIProfileInfoPartial(BaseModel):
    profile_name: str
    description: str
    service: str


class AIProfilePartialResponse(BaseModel):
    id: uuid.UUID
    profile_name: str

    model_config = ConfigDict(from_attributes=True)


class AIProfileFullResponse(BaseModel):
    id: uuid.UUID
    profile_name: str
    description: str
    service: str
    model_name: str

    model_config = ConfigDict(from_attributes=True)


class AIProfileResponse(BaseModel):
    id: uuid.UUID
    db_type: str
    json_props: dict

    model_config = ConfigDict(from_attributes=True)


class AIProfileInput(BaseModel):
    profile_name: str
    description: str
    service: SupportedServices
    model_name: str
    auth_token: str

    model_config = ConfigDict(from_attributes=True)


class AIProfileDeleteOutput(BaseModel):
    id: uuid.UUID
    model_config = ConfigDict(from_attributes=True)


class AIProfileUpdateInput(BaseModel):
    profile_name: str
    description: str
    service: SupportedServices
    model_name: str
    auth_token: str
