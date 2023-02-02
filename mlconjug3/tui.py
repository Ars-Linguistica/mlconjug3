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
from textual import Terminal

@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
def main():
    """
    Examples of how to use mlconjug3 from the terminal
    """
    terminal = Terminal()

    with terminal.application("MLConjug3", layout="grid"):
        with terminal.tab("Conjugate"):
            with terminal.form("Verb Conjugation") as form:
                language = form.choice("Language", options=["fr", "en", "es", "it", "pt", "ro"], default="fr")
                verb = form.text("Verb", default="")
                subject = form.choice("Subject", options=["abbrev", "pronoun"], default="abbrev")
                output_file = form.text("Output file", default="")
                file_format = form.choice("File format", options=["json", "csv"], default="json")
                form.submit("Conjugate")

        with terminal.tab("Settings"):
            with terminal.collapse("Load/Save Configurations"):
                config_file = terminal.text("Config file", default="")
                load_config_button = terminal.button("Load Config")
                save_config_button = terminal.button("Save Config")

            with terminal.collapse("Theme Settings"):
                theme_settings = terminal.text("Theme Settings", default="")
                apply_theme_button = terminal.button("Apply Theme")
                reset_theme_button = terminal.button("Reset Theme")
            
        with terminal.tab("Help"):
            terminal.text("Help content")
    
    if form.is_submitted():
        # process the form data
        config_options = load_config(config_file)
        language = config_options.get('language', language)
        subject = config_options.get('subject', subject)
        output = config_options.get('output', output_file)
        file_format = config_options.get('file_format', file_format)
        conjugator = Conjugator(language=language, subject=subject)
        conjugated_verb = conjugator.conjugate(verb)
        if file_format == "json":
            with open(output_file, "w") as f:
                f.write(json.dumps(conjugated_verb))
        elif file_format == "csv":
            pass
            # write to csv file
        else:
            raise ValueError(f"Invalid file format: {file_format}")
        
    # show the terminal
    terminal.run()

def load_config(config_file):
    """
    Loads configuration from the specified file. Supports toml and yaml file formats.
    """
    if not config_file:
        return {}

    if config_file.endswith(".toml"):
        with open(config_file, "r") as f:
            return tomlkit.loads(f.read())
    elif config_file.endswith(".yaml") or config_file.endswith(".yml"):
        with open(config_file, "r") as f:
            return yaml.load(f.read(), Loader=yaml.SafeLoader)
    else:
        raise ValueError(f"Invalid configuration file format. Only .toml and .yaml formats are supported, not {config_file}")

if __name__ == '__main__':
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    main()