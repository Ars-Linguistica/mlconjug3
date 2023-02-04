import sys
import os
import json
import tomlkit
import yaml
from rich.pretty import pprint, Pretty
from rich.table import Table
from rich.columns import Columns
import rich

import flutter
from flutter import Flutter

def main():
    fl = Flutter(as_theme=True)
    verbs = fl.input_string("Enter verbs separated by space:")
    language = fl.input_enum("Choose the language for the conjugation pipeline:", ["fr", "en", "es", "it", "pt", "ro"])
    subject = fl.input_enum("Choose the subject format:", ["abbrev", "pronoun"])
    output = fl.input_string("Enter the path of the filename for storing the conjugation tables:") or None
    file_format = fl.input_enum("Choose the output format:", ["json", "csv"])
    config = fl.input_file("Choose the configuration file:") or None
    
    config_options = load_config(config)
    language = config_options.get('language', language)
    subject = config_options.get('subject', subject)
    output = config_options.get('output', output)
    file_format = config_options.get('file_format', file_format)
    theme_settings = config_options.get('theme', {})
    
    conjugator = Conjugator(language)
    conjugations = {}
    missing = []
    
    verbs = verbs.split(" ")
    if len(verbs) == 1:
        result = conjugator.conjugate(verbs[0], subject)
        if result:
            conjugations[verbs[0]] = result
        else:
            missing.append(verbs[0])
    else:
        for verb in verbs:
            result = conjugator.conjugate(verb, subject)
            if result:
                conjugations[verb] = result
            else:
                missing.append(verb)
    
    if output:
        with open(output, "w") as f:
            if file_format == "json":
                json.dump(conjugations, f)
            elif file_format == "csv":
                table = Table(show_header=True, header_style="bold yellow")
                table.add_column("Verb")
                for form in conjugations[list(conjugations.keys())[0]].keys():
                    table.add_column(form)
                for verb in conjugations.keys():
                    row = [verb]
                    for form in conjugations[verb].values():
                        row.append(form)
                    table.add_row(*row)
                f.write(str(table))
    if missing:
        fl.alert("The following verbs are not found in the conjugation database: " + ", ".join(missing))
    if conjugations:
        table = Table(show_header=True, header_style="bold yellow")
        table.add_column("Verb")
        for form in conjugations[list(conjugations.keys())[0]].keys():
            table.add_column(form)
        for verb in conjugations.keys():
            row = [verb]
            for form in conjugations[verb].values():
                row.append(form)
                table.add_row(*row)
        pprint(table, **theme_settings)

        
def load_config(file_path):
    if not file_path:
        return {}
    if file_path.endswith(".json"):
        with open(file_path, "r") as f:
            return json.load(f)
    elif file_path.endswith(".toml"):
        with open(file_path, "r") as f:
            return tomlkit.parse(f.read())
    elif file_path.endswith(".yaml") or file_path.endswith(".yml"):
        with open(file_path, "r") as f:
            return yaml.safe_load(f)
    else:
        raise ValueError("Unsupported configuration file format.")

        
if name == "main":
    main()
