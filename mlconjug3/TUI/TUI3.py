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
    self.help_section.add(textual.Text("Enter a verb in the prompt to conjugate it. Use the export button to save the conjugations. Use the language selector to choose the language for conjugation. Use the subject selector to choose between abbrev or pronoun for conjugations"))
    def handle_submit(self, verb):
self.conjugator.set_language(self.language_selector.get_value())
conjugation_result = self.conjugator.conjugate(verb, self.subject_selector.get_value())
if conjugation_result:
self.verb_history.add_item(verb)
self.conjugation_tables.clear()
for tense, conjugations in conjugation_result.items():
tense_container = self.conjugation_tables.add(textual.Container())
tense_container.add(textual.Label(tense))
conjugation_table = tense_container.add(textual.Table(["Person", "Conjugation"]))
for conjugation in conjugations:
conjugation_table.add_row([conjugation[0], conjugation[1]])
else:
self.conjugation_tables.clear()
self.conjugation_tables.add(textual.Label("Invalid verb or verb not found"))
self.prompt.clear()
self.sample_verbs.clear()
self.sample_verbs.add_items(self.conjugator.get_similar_verbs(verb))
self.sample_verbs.on_select(self.handle_similar_verb_select)
self.app.focus(self.prompt)

def handle_similar_verb_select(self, verb):
self.prompt.set_value(verb)
self.handle_submit(verb)
self.app.focus(self.prompt)

def handle_export(self):
export_format = textual.dialog.ask("What format do you want to export?", ["JSON", "CSV"])
if export_format:
export_path = textual.dialog.ask("Where do you want to save the file?", "file")
if export_path:
with open(export_path, 'w', encoding='utf-8') as file:
json.dump(self.conjugation_tables, file, ensure_ascii=False, indent=4)
textual.alert("The conjugations have been succesfully saved to {0}.".format(export_path))
self.app.focus(self.export_button)

def handle_history_select(self, verb):
self.prompt.set_value(verb)
self.handle_submit(verb)
self.app.focus(self.prompt)

def handle_language_select(self, language):
self.conjugator.set_language(language)
self.app.focus(self.language_selector)

def handle_subject_select(self, subject):
self.handle_submit(self.prompt.get_value())
self.app.focus(self.subject_selector)

def run(self):
self.app.run()
