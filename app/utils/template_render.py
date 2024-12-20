from jinja2 import Environment, FileSystemLoader
import os


def render(folder: str, template_name: str, data: list[dict]) -> list[str]:
    print(folder)
    print(os.listdir(folder))
    environment = Environment(loader=FileSystemLoader(folder))
    print("render here")
    template = environment.get_template(template_name)

    return [template.render(x) for x in data]
