import logging
from ..providers.llm_service_provider import LLMServiceProvider
from routers.meta_extraction.managers.meta_extractor_manager import (
    MetaExtractorManager
)
from sqlalchemy.exc import SQLAlchemyError, OperationalError
from ..exceptions import DatabaseUnreachable, GenerationError


class MainGenerationStrategy:
    def __init__(
            self,
            llm_provider: LLMServiceProvider,
            executor: MetaExtractorManager
    ):
        self.llm_provider = llm_provider
        self.executor = executor
        self.error_prompt = """
            Your sql code has errors: <err>. Fix it.And send only code.
            Forbidden to send explanations
        """

    async def execute_generated_sql(self, sys_prompt: str, user_query: str):
        err = None
        n_err = None
        print("Start generating code")
        for i in range(3):

            if err:
                user_query = self.error_prompt.replace("<err>", err)
            
            print(f"LLM service is: {self.llm_provider}")

            generated_sql = await self.llm_provider.generate_sql(
                sys_prompt, user_query
            )

            generated_sql = generated_sql.generated

            if not generated_sql:
                logging.info(
                    f"{i} attempt failed - can not get result from service"
                )
                n_err = "No connection to service"
                continue
            
            print(f"GENERATED QUERY: {generated_sql}")
            exc_res, err_mes = await self.try_execute(generated_sql)

            if not exc_res and not err_mes:
                logging.exception("Database error occurred!")
                raise DatabaseUnreachable()

            if exc_res:
                self.generated_query = generated_sql
                return exc_res

            if err_mes:
                err = err_mes
        
        if err:
            logging.exception("Unable to generate")
            raise GenerationError()
        
        if n_err:
            logging.exception(n_err)
            raise GenerationError(n_err)

    async def try_execute(self, query: str):
        try:
            result = self.executor.execute_sql(query)
            return result, None
        except OperationalError as e:
            logging.exception(e)
            return None, None
        except Exception as e:
            logging.exception(e)
            return None, str(e)
