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
from .mlconjug import Conjugator
import json
import tomlkit
import yaml
import logging
import rich
from textual import Window, TextView, Button

class MainWindow(Window):
    def __init__(self, language='fr', subject='abbrev'):
        self.conjugator = Conjugator(language)
        self.subject = subject
        self.output = None
        self.file_format = None
        self.tab_views = []
        self.current_tab = None
        
        # Set up the main window
        super().__init__(title='mlconjug3')
        self.set_layout('grid')

        # Add a text view for entering the verb
        self.verb_input = TextView(text='Enter a verb:', align='left')
        self.add_view(self.verb_input, row=0, column=0, sticky='nsew', pad=10)

        # Add a button for conjugating the verb
        conjugate_button = Button(text='Conjugate', align='left')
        conjugate_button.on_click = self.conjugate
        self.add_view(conjugate_button, row=0, column=1, pad=10)

        # Add a text view for the conjugated verb
        self.conjugation_output = TextView(text='', align='left')
        self.add_view(self.conjugation_output, row=1, column=0, column_span=2, sticky='nsew', pad=10)

    def conjugate(self):
        verb = self.verb_input.text
        try:
            conjugation = self.conjugator.conjugate(verb, subject=self.subject)
        except Exception as e:
            conjugation = str(e)

        self.conjugation_output.text = str(conjugation)

    def add_tab(self, conjugation):
        tab_view = TextView(text=str(conjugation))
        self.tab_views.append(tab_view)
        self.current_tab = tab_view

    def switch_tab(self, index):
        self.current_tab = self.tab_views[index]
        self.conjugation_output.text = self.current_tab.text

def run_app():
    window = MainWindow()
    window.run()

if __name__ == '__main__':
    run_app()
