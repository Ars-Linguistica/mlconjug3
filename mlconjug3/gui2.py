from fastapi import FastAPI, Query, File, UploadFile
import os
import yaml
import htmx
from .mlconjug import Conjugator

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Conjugated Forms API"}

@app.post("/conjugate")
@htmx.html
async def conjugate(verb: str = Query(None, title="Verb"), 
             language: str = Query("fr", title="Language", description="The language to conjugate the verb in"), 
             subject: str = Query("abbrev", title="Subject", description="The subject format (full or abbrev)"), 
             file_format: str = Query("json", title="File Format", description="The format of the output file"), 
             config: UploadFile = File(None)):
    config_options = {}
    if config:
        config_file = await config.read()
        config_options = yaml.load(config_file, Loader=yaml.FullLoader)

    language = config_options.get('language', language)
    subject = config_options.get('subject', subject)
    file_format = config_options.get('file_format', file_format)

    if not verb:
        return """
            <html>
                <head>
                    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
                    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
                </head>
                <body>
                    <div class="container">
                        <div class="row">
                            <div class="col s12 m6 offset-m3">
                                <div class="card red lighten-5">
                                    <div class="card-content red-text">
                                        <span class="card-title">Error</span>
                                        <p>Please enter a verb to conjugate.</p>
                                    </div>
                                           </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </body>
            </html>
        """
    conjugator = Conjugator(language=language, subject=subject)
    conjugated_forms = conjugator.conjugate(verb)

    if file_format == "json":
        return {"verb": verb, "conjugated_forms": conjugated_forms}
    else:
        return {"message": "File format not supported"}
                        
def load_config(file_path):
    if not file_path:
        return {}
    if file_path.endswith(".json"):
        with open(file_path, "r") as f:
            return json.load(f)
    elif file_path.endswith(".toml"):
        with open(file_path, "r") as f:
            return tomlkit.parse(f.read())
    elif file_path.endswith(".yaml") or file_path.endswith(".yml"):
        with open(file_path, "r") as f:
            return yaml.safe_load(f)
    else:
        raise ValueError("Unsupported configuration file format.")
