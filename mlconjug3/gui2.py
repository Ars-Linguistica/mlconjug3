from fastapi import FastAPI
import os
import tomlkit
import yaml
import htmx
from .mlconjug import Conjugator

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Conjugator API"}

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
        <div class="container">
            <h1>Conjugated forms for "{verb}" in "{language}"</h1>
            <p>Subject format: {subject}</p>
            <p>Output format: {file_format}</p>
            <p>Conjugated forms: {conjugations}</p>
        </div>
    """

def load_config(config):
    """
    Loads the config file in the given format (toml or yaml).
    If no config file is specified, looks for a default file named 
    /mlconjug3/config.toml or /mlconjug3/config.yaml' in the user’s home directory.
    :param config: The path to the config file.
    :type config: str
    :return: A dictionary containing the configuration options.
    :rtype: dict
    """
    if not config:
        home = os.path.expanduser("~")
        config = os.path.join(home, 'mlconjug3/config.toml')
        if not os.path.isfile(config):
            config = os.path.join(home, 'mlconjug3/config.yaml')
            if not os.path.isfile(config):
                return {}
    config_options = {}
    if config.endswith('.toml'):
        with open(config, 'r') as config_file:
            config_options = tomlkit.loads(config_file.read())
    elif config.endswith('.yaml') or config.endswith('.yml'):
        with open(config, 'r') as config_file:
            config_options = yaml.load(config_file, Loader=yaml.FullLoader)
    return config_options
