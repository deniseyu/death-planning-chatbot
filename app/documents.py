import os
from jinja2 import Environment, FileSystemLoader

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates")

_env = Environment(loader=FileSystemLoader(TEMPLATE_DIR), autoescape=False)


def render_advance_directive(data: dict) -> str:
    """Render the advance directive Markdown from structured data."""
    template = _env.get_template("advance_directive.md")
    return template.render(**data)
