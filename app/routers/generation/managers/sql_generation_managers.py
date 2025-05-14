from uuid import UUID
from repository.tables_metadata import get_all_metadata
from repository.db_settings import get_db_connection


from ..models import GenerationInfoInput
from routers.metadata.models import TableMetadataResponse
from ..providers.llm_service_provider import LLMServiceProvider

from routers.meta_extraction.managers.meta_extractor_manager import (
    MetaExtractorManager
)
from ..promt_generation.full_ddl_prompt_generator import (
    FullDDLPromptGenerator
)
from ..strategies.main_generation_strategy import (
    MainGenerationStrategy
)


class SqlGenerationManager:
    def __init__(
            self,
            db, connection_id: UUID,
            i: GenerationInfoInput,
            llm_provider: LLMServiceProvider,
            crypt_service
    ):
        self.db = db
        self.con_id = connection_id
        self.gi = i
        self.generator = FullDDLPromptGenerator()
        self.llm_provider = llm_provider
        self.crypt_service = crypt_service

        self.prompt = None
        self.conn = None
        self.generated_query = None

    def _get_generator(self, type="ddl"):
        dct = {
            "ddl": FullDDLPromptGenerator
        }

        if type not in dct.keys():
            raise Exception("Invalid prompt generator type")

        return dct.get(type)

    async def generate_prompt(self) -> str:
        data = await get_all_metadata(self.db, self.con_id)
        prompt = self.generator.generate_prompt(
            user_query=self.gi.user_query,
            tables_info=[TableMetadataResponse.from_orm(x) for x in data]
        )
        self.prompt = prompt
        return prompt

    async def execute_generated_query(self) -> str:
        conn = self.conn
        if not conn:
            conn = await get_db_connection(
                self.db,
                self.con_id,
                self.crypt_service
            )
            self.conn = conn

        prompt = self.prompt
        if not prompt:
            prompt = await self.generate_prompt()

        m = MainGenerationStrategy(
            self.llm_provider,
            MetaExtractorManager(conn, reflect=False)
        )

        res = await m.execute_generated_sql(prompt, self.gi.user_query)
        self.generated_query = m.generated_query
        return res
