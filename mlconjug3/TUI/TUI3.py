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
