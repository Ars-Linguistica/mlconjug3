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

    ##################
    def display_conjugations_in_table(self, conjugations):
    self.conjugation_tables.clear()
    headers = ["Person", "Singular", "Plural"]
    rows = []
    for person, conjugation in conjugations.items():
        rows.append([person, conjugation["singular"], conjugation["plural"]])
    table = textual.Table(headers=headers, rows=rows)
    self.conjugation_tables.add(table)
    
    def change_verb_tense(self):
self.tense_selector = self.right_section.add(textual.Select(options=["present", "past", "future", "subjunctive", "conditional"]))
self.tense_selector.on_select(self.handle_tense_change)

    def handle_tense_change(self, selection):
    self.tense = selection
    self.handle_submit(self.verb_input.value)
    
    def compare_multiple_conjugations(self):
self.multiple_verb_input = self.left_section.add(textual.Prompt(placeholder="Enter multiple verbs separated by commas"))
self.multiple_verb_input.on_submit(self.handle_multiple_submit)

    def handle_multiple_submit(self, input_text):
    verbs = input_text.split(',')
    results = {}
    for verb in verbs:
        result = self.conjugator.conjugate(verb.strip(), self.subject)
        results[verb.strip()] = result.conjug_info
    self.conjugation_tables.clear()
    for verb, conjugations in results.items():
        verb_table = self.conjugation_tables.add(textual.Table(flex=1))
        verb_table.add_column("Tense/Person", flex=1)
        verb_table.add_column(verb, flex=1)
        for tense, conjugation in conjugations.items():
            verb_table.add_row(tense, conjugation)
    self.verb_history.append(input_text)
    
    def filter_conjugations_by_person_number_mood(self, verb_info, person, number, mood):
filtered_conjugations = {}
for key, value in verb_info.conjug_info.items():
if key.endswith(person + number + mood):
filtered_conjugations[key] = value
return filtered_conjugations

def handle_filter_select(self, person, number, mood):
verb_info = self.verb_history.get_selected()
filtered_conjugations = self.filter_conjugations_by_person_number_mood(verb_info, person, number, mood)
self.conjugation_tables.clear()
self.conjugation_tables.add(textual.Text(json.dumps(filtered_conjugations, ensure_ascii=False, indent=4)))
self.app.render()

Add the filter selections to the user interface, such as dropdown menus for person, number, and mood

self.person_selector = self.right_section.add(textual.Select(options=["1st", "2nd", "3rd"]))
self.number_selector = self.right_section.add(textual.Select(options=["singular", "plural"]))
self.mood_selector = self.right_section.add(textual.Select(options=["indicative", "subjunctive", "conditional", "imperative"]))

Handle the user's selections for person, number, and mood

self.person_selector.on_select(partial(self.handle_filter_select, person=self.person_selector.get_selected()))
self.number_selector.on_select(partial(self.handle_filter_select, number=self.number_selector.get_selected()))
self.mood_selector.on_select(partial(self.handle_filter_select, mood=self.mood_selector.get_selected()))

Add a "Filter" button for the user to initiate the filtering process

self.filter_button = self.right_section.add(textual.Button("Filter"))
self.filter_button.on_click(partial(self.handle_filter_select, person=self.person_selector.get_selected(), number=self.number_selector.get_selected(), mood=self.mood_selector.get_selected()))

Add a "Clear Filter" button for the user to clear any applied filters and view the full conjugation table again

self.clear_filter_button = self.right_section.add(textual.Button("Clear Filter"))
self.clear_filter_button.on_click(self.handle_clear_filter)

def handle_clear_filter(self):
verb_info = self.verb_history.get_selected()
self.conjugation_tables.clear()
self.conjugation_tables.add(textual.Text(json.dumps(verb_info.conjug_info, ensure_ascii=False, indent=4)))
self.app.render()

    def change_font_size_and_type(self, font_size, font_type):
"""
Allows users to change the font size and type for the conjugations.
This would make it easier for users with visual impairments to read the conjugations.
:param font_size: int. The desired font size for the conjugations
:param font_type: string. The desired font type for the conjugations
"""
self.conjugation_tables.style.font_size = font_size
self.conjugation_tables.style.font_type = font_type
self.app.refresh()

    def save_conjugation_history(self, verb, conjugations):
"""
Save the conjugation history in a list and display it in the verb history section of the TUI
:param verb: str, the verb that was conjugated
:param conjugations: dict, the conjugations of the verb
"""
self.verb_history.append(verb)
self.conjugation_history[verb] = conjugations
self.verb_history.update()

def handle_history_select(self, verb):
"""
Handle the select event of the verb history, by displaying the conjugations of the selected verb
:param verb: str, the verb that was selected
"""
self.conjugation_tables.clear()
conjugations = self.conjugation_history[verb]
for key, value in conjugations.items():
self.conjugation_tables.add(textual.Text("{}: {}".format(key, value)))
self.conjugation_tables.update()

def handle_export(self):
"""
Handle the click event of the export button, by saving the conjugation history to a file
"""
with open("conjugation_history.json", "w") as file:
json.dump(self.conjugation_history, file)
self.help_section.clear()
self.help_section.add(textual.Text("Conjugation history has been saved to conjugation_history.json"))
self.help_section.update()

def init_help_section(self):
"""
Initialize the help section with instructions on how to use the TUI
"""
self.help_section.add(textual.Text("Enter a verb in the prompt to conjugate it."))
self.help_section.add(textual.Text("Use the export button to save the conjugations."))
self.help_section.add(textual.Text("Use the language selector to choose the language for conjugation."))
self.help_section.add(textual.Text("Use the subject selector to choose between abbrev or pronoun for conjugations"))
self.help_section.add(textual.Text("Use the verb history section to view previous conjugations"))
self.help_section.update()

def run(self):
"""
Start the TUI
"""
self.app.run()

def init(self):
self.conjugation_history = {}
self.init()

def del(self):
self.app.exit()

    def compare_conjugations_multiple_languages(self, verb):
"""
Compares the conjugations of the given verb in multiple languages by conjugating the verb for all languages and displaying the conjugations in the conjugation_tables widget
"""
self.conjugation_tables.clear()
for language in self.language_selector.options:
self.conjugator.set_language(language)
conjugations = self.conjugator.conjugate(verb, self.subject_selector.value)
self.conjugation_tables.add(textual.Text(f"Conjugations for {verb} in {language}:"))
for key, value in conjugations.items():
self.conjugation_tables.add(textual.Text(f"{key}: {value}"))
