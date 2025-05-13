
from jinja2 import Environment, FileSystemLoader
from loguru import logger


def render(folder: str, template_name: str, data: list[dict]) -> list[str]:
    logger.info("start rendering")
    environment = Environment(loader=FileSystemLoader(folder))
    template = environment.get_template(template_name)

    return [template.render(x) for x in data]
