from .promt_generator import IPromptGenerator
from utils.template_render import render
from pydantic import BaseModel
import os


class FullDDLPromptGenerator(IPromptGenerator):
    def __init__(self):
        self.folder = self._get_templates_dir()
        self.template_name = "create_table.twig"
        self.prefix = """You are helpful assistant
        which generates SQL for PostgresSQL only"""
        self.link = """These are tables structure"""

    def _get_templates_dir(self) -> str:
        return os.path.abspath(
            f"routers{os.sep}generation{os.sep}templates")

    def generate_prompt(self, **kwargs) -> str:
        """
        @params: user_query
        @params: tables_info
        """
        tables_data: list[BaseModel] = kwargs.get("tables_info")
        print("here")
        rendered_data = "\n".join(render(
            self.folder,
            self.template_name,
            [x.model_dump() for x in tables_data]
        ))
        return f"{self.prefix}\n{self.link}\n{rendered_data}"
