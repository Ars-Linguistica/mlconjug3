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
import textual
from .mlconjug import Conjugator
import json
import tomlkit
import yaml
import logging

def main():
    # create a Textual App instance
    app = textual.App(title="mlconjug3")

    # create a prompt to enter verb to conjugate
    prompt = textual.Prompt("Enter a verb to conjugate:", default="aimer")
    verb = prompt.get()

    # create a tabbed panel for conjugation tables
    conjugation_tabs = textual.TabbedPanel()

    # create a collapsible widget to display the conjugation table
    conjugation_table = textual.CollapsibleWidget("Conjugation table")

    # add the verb conjugation table to the collapsible widget
    conjugation_table.add(get_conjugation_table(verb))

    # add the collapsible widget to the tabbed panel
    conjugation_tabs.add(conjugation_table, title=verb)

    # add the tabbed panel to the app
    app.add(conjugation_tabs)

    # create a button to replicate the functionality of saving the conjugation tables
    save_button = textual.Button("Save", action=save_conjugation_table)

    # add the button to the app
    app.add(save_button)

    # create a menu to replicate the functionality of choosing the language, subject type, saving options, as well as setting a theme and saving loading settings
    settings_menu = textual.Menu("Settings")

    # add the menu options to the menu
    settings_menu.add("Choose language", action=choose_language)
    settings_menu.add("Choose subject type", action=choose_subject_type)
    settings_menu.add("Save options", action=save_options)
    settings_menu.add("Set theme", action=set_theme)
    settings_menu.add("Save/Load settings", action=save_load_settings)

    # add the menu to the app
    app.add(settings_menu)

    # run the app
    app.run()

def get_conjugation_table(verb):
    """Get the conjugation table for the verb"""
    conjugator = Conjugator()
    conjugation_data = conjugator.conjugate(verb)
    # format the conjugation data as a table
    table = ...
    return table

def save_conjugation_table():
    """Save the conjugation table to a file"""
    pass

def choose_language():
    """Choose the language for the conjugation pipeline"""
    pass

def choose_subject_type():
    """Choose the subject format type for the conjugated forms"""
    pass

def save_options():
    """Save the options for the conjugation pipeline"""
    pass

def set_theme():
    """Set the theme for the conjugation table columns"""
    pass
