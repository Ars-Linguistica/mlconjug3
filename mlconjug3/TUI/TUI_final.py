import textual
from .mlconjug import Conjugator
import json
import logging
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from PIL import Image, ImageDraw, ImageFont
import requests
from bs4 import BeautifulSoup


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
        self.grid_view_button = self.right_section.add(textual.Button("Grid View"))
        self.image_view_button = self.right_section.add(textual.Button("Image View"))
        self.grid_view_button.on_click(self.handle_grid_view)
        self.image_view_button.on_click(self.handle_image_view)
        self.help_section = self.right_section.add(textual.Container(flex=1))
        self.app.add_stylesheet("dark.css")
        self.add_dark_mode_button()

        self.conjugator = Conjugator()
        self.prompt.on_submit(self.handle_submit)
        self.export_button.on_click(self.handle_export)
        self.verb_history.on_select(self.handle_history_select)
        self.language_selector.on_select(self.handle_language_select)
        self.subject_selector.on_select(self.handle_subject_select)
        self.help_section.add(textual.Text("Enter a verb in the prompt to conjugate it. Use the export button to save the conjugations. Use the language selector to choose the language for conjugation. Use the subject selector to choose between abbrev or pronoun for conjugations"))
        
    @staticmethod
    def get_verb_examples_in_context(verb):
        """
        Retrieves examples of the provided verb used in context from an external website.
        :param verb: string. The verb to retrieve examples for.
        :return: list of strings. A list of examples of the verb used in context.
        """
        url = f"https://context.reverso.net/translation/{verb}-examples"
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        examples = soup.find_all("a", class_="example-sentence")
        return [example.get_text() for example in examples]
  
def handle_submit(self, verb):
    self.conjugator.language = self.language
    conjugations = self.conjugator.conjugate(verb, self.subject)
    self.conjugation_tables.clear()
    verb_table = self.conjugation_tables.add(textual.Table(flex=1))
    verb_table.add_column("Tense/Person", flex=1)
    verb_table.add_column(verb, flex=1)
    for tense, conjugation in conjugations.conjug_info.items():
        verb_table.add_row(tense, conjugation)
    self.verb_history.append(verb)
    self.save_conjugation_history(verb, self.language, self.subject)

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
    
def handle_filter_select(self, selector, person, number, mood):
    selected_verb = self.verb_history.get_selected()
    if selected_verb:
        conjugations = self.filter_conjugations_by_person_number_mood(selected_verb, person, number, mood)
        self.conjugation_tables.clear()
        verb_table = self.conjugation_tables.add(textual.Table(flex=1))
        verb_table.add_column("Tense/Person", flex=1)
        verb_table.add_column(selected_verb.verb, flex=1)
        for tense, conjugation in conjugations.items():
            verb_table.add_row(tense,

def handle_export(self):
conjugations = {}
for verb_table in self.conjugation_tables.components:
verb = verb_table.columns[1].title
conjugations[verb] = {}
for row in verb_table.rows:
tense_person = row[0]
conjugation = row[1]
conjugations[verb][tense_person] = conjugation
with open("conjugations.json", "w") as outfile:
json.dump(conjugations, outfile)
self.app.alert("Conjugations exported to conjugations.json")

def handle_history_select(self, verb):
self.prompt.input = verb
self.handle_submit(verb)

def handle_language_select(self, language):
self.language = language

def handle_subject_select(self, subject):
self.subject = subject

def handle_grid_view(self):
self.template = self.template_selector.get_value()
self.conjugation_tables.clear()
for verb, conjugations in self.conjugations.items():
verb_table = self.conjugation_tables.add(textual.Table(flex=1))
verb_table.add_column("Tense/Person", flex=1)
verb_table.add_column(verb, flex=1)
for tense, conjugation in conjugations.items():
verb_table.add_row(tense, conjugation)
self.app.render()

def handle_image_view(self):
self.template = self.template_selector.get_value()
self.conjugation_tables.clear()
for verb, conjugations in self.conjugations.items():
conjugations_image = self.create_conjugations_image(verb, conjugations)
self.conjugation_tables.add(textual.Image(conjugations_image))
self.app.render()

def add_dark_mode_button(self):
self.dark_mode_button = self.right_section.add(textual.Button("Dark Mode"))
self.dark_mode_button.on_click(self.handle_dark_mode)

def handle_dark_mode(self):
if self.app.stylesheet == "dark.css":
self.app.stylesheet = ""
else:
self.app.stylesheet = "dark.css"
self.app.render()

def create_conjugations_image(self, verb, conjugations):
image = Image.new("RGB", (800, 600), (255, 255, 255))
draw = ImageDraw.Draw(image)
font = ImageFont.truetype("arial.ttf", 16)
x = 50
y = 50
draw.text((x, y), f"Conjugations for {verb}", (0, 0, 0), font=font)
y += 50
      
