from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
import json
import tomlkit
import yaml
from mlconjug3 import Conjugator

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "title": "mlconjug3 - Conjugation Tables"
    })

@app.post("/conjugate")
async def conjugate(request: Request, verb: str, language: str, subject: str, output: str, file_format: str, config: str):
    config_options = load_config(config)
    language = config_options.get('language', language)
    subject = config_options.get('subject', subject)
    output = config_options.get('output', output)
    file_format = config_options.get('file_format', file_format)
    theme_settings = config_options.get('theme', {})

    conjugator = Conjugator(language, subject, output, file_format, theme_settings)
    conjugation_table = conjugator.conjugate(verb)

    return templates.TemplateResponse("conjugation.html", {
        "request": request,
        "verb": verb,
        "language": language,
        "subject": subject,
        "output": output,
        "file_format": file_format,
        "config": config,
        "conjugation_table": conjugation_table
    })

def load_config(config):
    if config is None:
        return {}
    if config.endswith(".toml"):
        with open(config, "r") as f:
            return tomlkit.parse(f.read())
    elif config.endswith(".yaml") or config.endswith(".yml"):
        with open(config, "r") as f:
            return yaml.safe_load(f)
    else:
        raise Exception("Invalid config file format")
