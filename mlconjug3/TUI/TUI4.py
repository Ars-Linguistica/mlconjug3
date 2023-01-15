import textual
from .mlconjug import Conjugator
import json
import logging

import requests
from bs4 import BeautifulSoup

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
                conjugation_table = tense_container.add(textual.Table(headers=["Subject", "Conjugation"]))
                for subject, conjugation in conjugations.items():
                    conjugation_table.add_row([subject, conjugation])
                examples = get_verb_examples_in_context(verb)
                if examples:
                    self.sample_verbs.clear()
                    for example in examples:
                        self.sample_verbs.add_item(example)
                else:
                    self.conjugation_tables.clear()
                    self.conjugation_tables.add(textual.Text("The verb is not in the dataset. The conjugation was not possible."))

    def handle_export(self):
        """
        Handles the export button click event.
        Exports the conjugation tables to a json file.
        """
        verb_conjugations = {}
        for i in range(self.verb_history.count()):
            verb = self.verb_history.get_item(i)
            conjugation_result = self.conjugator.conjugate(verb, self.subject_selector.get_value())
            verb_conjugations[verb] = conjugation_result
        with open("conjugations.json", "w") as file:
            json.dump(verb_conjugations, file)
        self.app.show_message("Conjugations exported to conjugations.json")

    def handle_history_select(self, verb):
        """
        Handles the verb history list select event.
        Displays the conjugations for the selected verb.
        """
        self.prompt.set_text(verb)
        conjugation_result = self.conjugator.conjugate(verb, self.subject_selector.get_value())
        if conjugation_result:
            self.conjugation_tables.clear()
            for tense, conjugations in conjugation_result.items():
                tense_container = self.conjugation_tables.add(textual.Container())
                tense_container.add(textual.Label(tense))
                conjugation_table = tense_container.add(textual.Table(headers=["Subject", "Conjugation"]))
                for subject, conjugation in conjugations.items():
                    conjugation_table.add_row([subject, conjugation])
        else:
            self.conjugation_tables.clear()
            self.conjugation_tables.add(textual.Text("The verb is not in the dataset. The conjugation was not possible."))


    
