from rich.console import Console
from rich.table import Table
from textual import Input, Password

console = Console()

# Initialize the Conjugator with a specific language and feature extractor
conjugator = Conjugator(language='fr', feature_extractor=VerbFeatures())

# Prompt the user for input
verb = Input("Enter a verb to conjugate: ").ask()

# Conjugate the verb
verb_obj = conjugator.conjugate(verb)

# Display the conjugated forms in a table
table = Table(title="Conjugated Forms of '{}'".format(verb))
table.add_column("Mood")
table.add_column("Tense")
table.add_column("Person")
table.add_column("Form")

for mood, tense, person, form in verb_obj.iterate():
    table.add_row(mood, tense, person, form)

console.print(table)
