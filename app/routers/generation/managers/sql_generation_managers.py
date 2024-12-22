from uuid import UUID
from repository.tables_metadata import get_all_metadata
from repository.db_settings import get_db_connection

from integrations.llm_service.api import generate_lamini
from integrations.llm_service.models import LaminiInput
from ..models import GenerationInfoInput
from routers.metadata.models import TableMetadataResponse

from routers.meta_extraction.managers.meta_extractor_manager import (
    MetaExtractorManager
)
from ..promt_generation.full_ddl_prompt_generator import (
    FullDDLPromptGenerator
)


class SqlGenerationManager:
    def __init__(self, db, connection_id: UUID, i: GenerationInfoInput):
        self.db = db
        self.con_id = connection_id
        self.gi = i
        self.generator = FullDDLPromptGenerator()

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

    async def generate_sql(self) -> str:
        prompt = self.prompt
        if not prompt:
            prompt = await self.generate_prompt()
        result = await generate_lamini(
            params=LaminiInput(
                query=self.gi.user_query,
                prompt=prompt
            )
        )
        if not result:
            raise Exception("unable to complete request to LLM_Service")
        self.generated_query = result.generated
        return result.generated

    async def execute_generated_query(self) -> str:
        g_q = self.generated_query
        conn = self.conn
        if not g_q:
            g_q = await self.generate_sql()

        if not conn:
            conn = await get_db_connection(self.db, self.con_id)
            self.conn = conn

        m = MetaExtractorManager(conn, reflect=False)
        try:
            result = m.execute_sql(g_q)
        except Exception as e:
            print(e)
            result = m.execute_sql("select * from video_games.genre;")
            return result
