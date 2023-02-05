from fastapi import FastAPI, Request
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles
from .mlconjug import Conjugator
import json
import tomlkit
import yaml
import logging
from rich.pretty import pprint, Pretty
from rich.table import Table
from rich.columns import Columns
from rich.console import Console
import rich

app = FastAPI()

@app.get("/")
async def root(request: Request):
    return HTMLResponse("""
    <html>
        <body>
            <form action="/result" method="post">
                <input type="text" name="verb">
                <input type="submit" value="Conjugate">
                <br>
                <label for="language">Language:</label>
                <select id="language" name="language">
                  <option value="fr">French</option>
                  <option value="en">English</option>
                  <option value="es">Spanish</option>
                  <option value="it">Italian</option>
                  <option value="pt">Portuguese</option>
                  <option value="ro">Romanian</option>
                </select>
                <br>
                <label for="subject">Subject Type:</label>
                <select id="subject" name="subject">
                  <option value="abbrev">Abbreviated</option>
                  <option value="pronoun">Pronoun</option>
                </select>
                <br>
                <input type="submit" value="Save to disk">
            </form> 
        </body>
    </html>
    """)

@app.post("/result")
async def result(verb: str, language: str = "fr", subject: str = "abbrev"):
    conjugator = Conjugator(language, subject)
    conjugation_table = conjugator.conjugate(verb)
    table = Table(show_header=True, header_style="bold blue")
    table.add_column("Tense", style="dim", width=20)
    table.add_column("Forms", style="dim", width=80)
    for tense, forms in conjugation_table.items():
        table.add_row(tense, ", ".join(forms))
    return HTMLResponse(str(table))

if __name__ == "__main__":
    app.run()
