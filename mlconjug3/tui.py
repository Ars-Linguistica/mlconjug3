"""
This is a Text User Interface (TUI) module that provides a terminal-based interface to the MLConjug3 verb conjugation library.

The TUI uses the click library to build the command line interface and rich library to build the terminal interface. The TUI allows users to:

Conjugate verbs in various languages (French, English, Spanish, Italian, Portuguese, and Romanian)
Specify the language and subject (abbreviation or pronoun) for verb conjugation
Save and load configuration options in either toml or yaml file format
Apply custom themes to the terminal interface
The TUI also provides a help tab with general information on how to use the application.

The main function is the entry point to the TUI, it creates the terminal interface using rich library and launches the TUI using terminal.run().

The load_config function loads the configuration from a specified file in either toml or yaml format.

"""

import sys
import os
import click
from .mlconjug import Conjugator
import json
import tomlkit
import yaml
import logging
import rich

from textual.app import App, ComposeResult
from textual.containers import Container
from textual.reactive import reactive
from textual.widgets import Button, Header, Footer, Static, InputBox, Label


class ConjugationDisplay(Static):
    """A widget to display conjugation of a verb."""

    def __init__(self, verb: str, conjugator: Conjugator):
        self.verb = verb
        self.conjugator = conjugator
        self.conjugations = self.conjugator.conjugate(verb)

    @reactive
    def watch_verb(self, verb: str) -> None:
        """Called when the verb attribute changes."""
        self.verb = verb
        self.conjugations = self.conjugator.conjugate(verb)
        self.update(self.conjugations)

    def compose(self) -> ComposeResult:
        """Create child widgets of a conjugation display."""
        yield Label("Conjugations:")
        for tense, forms in self.conjugations.items():
            yield Label(f"{tense}:")
            for form, conjugation in forms.items():
                yield Label(f"{form}: {conjugation}")

class VerbInputBox(InputBox):
    """A widget for entering a verb to conjugate."""

    def __init__(self, conjugator: Conjugator):
        self.conjugator = conjugator

    def on_input(self, text: str) -> None:
        """Event handler called when the user submits the verb."""
        verb = text.strip()
        if verb:
            conjugation_display = self.query_one(ConjugationDisplay)
            conjugation_display.watch_verb(verb)
            self.clear()

class ConjugatorApp(App):
    """A Textual app to conjugate verbs."""

    def __init__(self, conjugator: Conjugator):
        self.conjugator = conjugator

    def compose(self) -> ComposeResult:
        """Called to add widgets to the app."""
        yield Header()
        yield Footer()
        yield VerbInputBox(self.conjugator)
        yield ConjugationDisplay("", self.conjugator)

if __name__ == "__main__":
    conjugator = Conjugator()
    app = ConjugatorApp(conjugator)
    app.run()
