from fastapi import FastAPI
from .mlconjug import Conjugator
import htmx

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/conjugate")
@htmx.html
def conjugate(verb: str, language: str = 'fr', subject: str = 'abbrev', file_format: str = 'json', config: str = None):
    config_options = load_config(config)
    language = config_options.get('language', language)
    subject = config_options.get('subject', subject)
    file_format = config_options.get('file_format', file_format)
    theme_settings = config_options.get('theme', {})

    conjugator = Conjugator(language)
    conjugations = conjugator.conjugate(verb)

    return f"""
        <div>
            <h1>Conjugated forms for {verb} in {language}</h1>
            <p>Subject format: {subject}</p>
            <p>Output format: {file_format}</p>
            <p>Conjugated forms: {conjugations}</p>
        </div>
    """
