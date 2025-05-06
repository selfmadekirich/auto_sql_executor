from pydantic import BaseModel
from .models import (
    AIProfileFullResponse,
    AIProfilePartialResponse,
    AIProfilesOptionValues,
    SupportedModels
)


def wrap_values(lst: list, flag_value: AIProfilesOptionValues):
    match flag_value:
        case AIProfilesOptionValues.all:
            return [AIProfileFullResponse.from_orm(x) for x in lst]
        case AIProfilesOptionValues.partly:
            return [AIProfilePartialResponse.from_orm(x) for x in lst]
    return None


def get_supported_models(service: str):
    lst = [x.value for x in SupportedModels
           if x.name == service]
    return lst[0] if lst else []


def check_model_is_supported(data: BaseModel):
    model_name = getattr(data, "model_name")
    service_name = getattr(data, "service")

    return model_name in get_supported_models(service_name)
