import textual
from .mlconjug import Conjugator
import json
import logging

class TUI:
def init(self):
self.app = textual.Application(title="Verb Conjugator")
self.left_section = self.app.add(textual.Container(flex=1))
self.right_section = self.app.add(textual.Container(flex=1))
self.prompt = self.left_section.add(textual.Prompt(placeholder="Enter a verb"))
self.conjugation_tables = self.left_section.add(textual.Container(flex=1))
self.verb_history = self.right_section.add(textual.List(flex=1))
self.sample_verbs = self.right_section.add(textual.List(flex=1))
self.export_button = self.right_section.add(textual.Button("Export"))
self.language_selector = self.right_section.add(textual.Select(options=["fr", "en", "es", "it", "pt", "ro"]))
self.subject_selector = self.right_section.add(textual.Select(options=["abbrev", "pronoun"]))
self.help_section = self.right_section.add(textual.Container(flex=1))
self.conjugator = Conjugator()
self.prompt.on_submit(self.handle_submit)
self.export_button.on_click(self.handle_export)
self.verb_history.on_select(self.handle_history_select)
self.language_selector.on_select(self.handle_language_select)
self.subject_selector.on_select(self.handle_subject_select)
def handle_submit(self, verb_string):
verbs = verb_string.split(",")
for verb in verbs:
verb = verb.strip()
conjugations = self.conjugator.conjugate(verb, subject=self.subject_selector.value)
table = self.create_conjugation_table(verb, conjugations)
self.conjugation_tables.add(table)
self.verb_history.append(verb)

def create_conjugation_table(self, verb, conjugations):
table = textual.Table()
table.append(["Tense", "Mood", "Person", "Conjugation"])
for tense, moods in conjugations.items():
for mood, persons in moods.items():
for person, conjugation in persons.items():
table.append([tense, mood, person, conjugation])
table.on_select(self.handle_table_select)
return table

def handle_table_select(self, row):
tense = row[0]
mood = row[1]
# hide the corresponding rows in all tables that have the same tense and mood
for table in self.conjugation_tables.children:
for r in table.children:
if r[0] == tense and r[1] == mood:
r.hide()

def handle_export(self):
data = {}
for table in self.conjugation_tables.children:
verb = table.label
conjugations = {}
for row in table.children:
tense = row[0]
mood = row[1]
person = row[2]
conjugation = row[3]
if tense not in conjugations:
conjugations[tense] = {}
if mood not in conjugations[tense]:
conjugations[tense][mood] = {}
conjugations[tense][mood][person] = conjugation
data[verb] = conjugations
format = self.app.prompt("Select export format", options=["JSON", "CSV"])
if format == "JSON":
    with open("conjugations.json", "w") as file:
        json.dump(data, file)
elif format == "CSV":
    pass  # add code for exporting to CSV
def handle_history_select(self, verb):
for table in self.conjugation_tables.children:
if table.label == verb:
table.show()
return
conjugations = self.conjugator.conjugate(verb, subject=self.subject_selector.value)
table = self.create_conjugation_table(verb, conjugations)
self.conjugation_tables.add(table)

def run(self):
self.app.run()

if name == "main":
tui = TUI()
tui.run()
