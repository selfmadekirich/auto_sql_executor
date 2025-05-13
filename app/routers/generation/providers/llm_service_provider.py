from routers.ai_profile.models import AIProfileInfoFull, SupportedServices
from ..exceptions import UnknownAIProfile
from loguru import logger
from integrations.llm_service.api import (
    generate_lamini, generate_openrouter, generate_groq
)


class LLMServiceProvider:
    def __init__(self, profile: AIProfileInfoFull):
        if not profile:
            raise UnknownAIProfile()

        self.profile = profile
        self.provider = self.get_provider_func()

        logger.info(f"profile is: {self.profile}")
        logger.info(f"self provider: {self.provider}")

    def get_provider_func(self):
        match self.profile.service:
            case SupportedServices.OpenRouter: return generate_openrouter
            case SupportedServices.Groq: return generate_groq
            case SupportedServices.Custom: return generate_lamini

    async def generate_sql(self, sys_promt: str, user_query: str):
        return await self.provider(sys_promt, user_query, self.profile)
