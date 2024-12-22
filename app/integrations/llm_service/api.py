from utils.http_service import post
from .models import LaminiInput, LaminiOutput
from settings import get_settings


async def generate_lamini(params: LaminiInput) -> LaminiOutput:
    try:
        host = get_settings().LLM_SERVICE_HOST
        port = get_settings().LLM_SERVICE_PORT
        result = await post(
            f"http://{host}:{port}/lamini/predict",
            params=params.model_dump(),
            headers={
                "Content-Type": "application/json"
            }
        )
        print(result.json())
        return LaminiOutput(**result.json())
    except Exception as e:
        print(e)
        return None
