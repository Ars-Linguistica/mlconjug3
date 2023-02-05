
from .mlconjug import Conjugator

from fastapi import FastAPI
from fastapi import UploadFile
from fastapi import File
from fastapi import Form
from fastapi.responses import HTMLResponse
import htmx

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/conjugate")
def conjugate(
    verb: str,
    language: str = "fr",
    subject: str = "abbrev",
    output: str = None,
    file_format: str = "json",
    config: UploadFile = File(None)
):
    conjugator = Conjugator()
    conjugator.conjugate(verb, language, subject)

    if file_format == "json":
        conjugator.to_json(output)
    elif file_format == "csv":
        conjugator.to_csv(output)

    table = Table(
        title="Conjugation Table for {}".format(verb),
        show_header=True,
        show_footer=True,
        header_style="bold green",
        footer_style="bold red",
        padding=(0, 1),
        style="round",
    )

    table.add_column("Subject")
    for form in conjugator.forms:
        table.add_column(form)

    for subject, forms in conjugator.conjugation.items():
        row = [subject]
        for form in conjugator.forms:
            row.append(forms[form])
        table.add_row(*row)

    html_table = table._repr_html_()
    return HTMLResponse(content=html_table, status_code=200)

