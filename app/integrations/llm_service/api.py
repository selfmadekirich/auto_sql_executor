import json
from utils.http_service import post_json
from loguru import logger
from .models import (
    LaminiInput,
    BasicOutput
)
from settings import get_settings
from routers.ai_profile.models import AIProfileInfoFull
from openai import OpenAI
from groq import Groq


async def generate_lamini(
        sys_prompt: str,
        user_query: str,
        profile: AIProfileInfoFull
) -> BasicOutput:
    
    try:
        logger.info("send request to custom service")
        params = LaminiInput(
            query=user_query,
            prompt=sys_prompt
        )
        host = get_settings().LLM_SERVICE_HOST
        port = get_settings().LLM_SERVICE_PORT
        result = await post_json(
            f"http://{host}:{port}/llama/predict",
            params=params.model_dump(),
            headers={
                "Content-Type": "application/json"
            }
        )

        logger.debug(result.json())
        return BasicOutput(**result.json())
    except Exception as e:
        logger.exception(e)
        return None


async def generate_openrouter(
        sys_prompt: str,
        user_query: str,
        profile: AIProfileInfoFull) -> BasicOutput:
    try:
        logger.info("sending message to openrouter")
        client = OpenAI(
            base_url=get_settings().OPENROUTER_SERVICE_HOST,
            api_key=profile.auth_token,
        )
        completion = client.chat.completions.create(
              model=profile.model_name,
              messages=[
                    {
                        "role": "system",
                        "content": sys_prompt
                    },
                    {
                        "role": "user",
                        "content": user_query
                    }
              ]
        )
        result = completion.choices[0].message.content
        logger.info(f"result:{result}")
        return BasicOutput(generated=result)
    except Exception as e:
        logger.exception(e)
        return None


async def generate_groq(
        sys_prompt: str,
        user_query: str,
        profile: AIProfileInfoFull) -> BasicOutput:
    try:
        logger.info("sending message to groq")

        client = Groq(
              api_key=profile.auth_token,
        )

        if "json" not in sys_prompt:
            sys_prompt = f"{sys_prompt} Put generated query in JSON."

        completion = client.chat.completions.create(
              model=profile.model_name,
              messages=[
                    {
                        "role": "system",
                        "content": sys_prompt
                    },
                    {
                        "role": "user",
                        "content": user_query
                    }
              ],
              temperature=1,
              max_completion_tokens=1024,
              top_p=1,
              stream=False,
              response_format={"type": "json_object"},
              stop=None,
        )
        result = completion.choices[0].message.content
        result = json.loads(result)
        logger.debug(f"result:{result}")
        return BasicOutput(generated=result.get(*result.keys()))
    except Exception as e:
        logger.exception(e)
        return BasicOutput(generated=None)
