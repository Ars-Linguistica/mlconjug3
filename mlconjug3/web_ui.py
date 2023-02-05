from fastapi import FastAPI
import htmx
from .mlconjug import Conjugator

app = FastAPI()

@app.get("/")
def index():
    input_field = htmx.Input(type="text", id="verb_input", name="verb_input")
    language_select = htmx.Select(id="language_select", name="language_select", options=["fr", "en", "es", "it", "pt", "ro"])
    subject_select = htmx.Select(id="subject_select", name="subject_select", options=["abbrev", "pronoun"])
    save_button = htmx.Button(id="save_button", type="button", content="Save Conjugation Table")
    conjugation_display = htmx.Div(id="conjugation_display")

    return f"""
    <html>
        <head>
            {htmx.js_include()}
        </head>
        <body>
            <div>
                <label for="verb_input">Enter Verb:</label>
                {input_field}
            </div>
            <div>
                <label for="language_select">Select Language:</label>
                {language_select}
            </div>
            <div>
                <label for="subject_select">Select Subject Format:</label>
                {subject_select}
            </div>
            <div>
                {save_button}
            </div>
            <div>
                {conjugation_display}
            </div>
        </body>
    </html>
    """

@app.post("/conjugate")
def conjugate(verb: str, language: str, subject: str):
    conjugator = Conjugator(language=language, subject=subject)
    conjugation_table = conjugator.conjugate(verb)
    return {"conjugation_table": conjugation_table}

@app.post("/save")
def save(verb: str, language: str, subject: str, file_format: str):
    conjugator = Conjugator(language=language, subject=subject, file_format=file_format)
    conjugator.conjugate_and_save(verb)
    return {"message": f"Conjugation table for verb {verb} saved to disk in {file_format} format."}
