"""Console script for mlconjug3."""

import sys
import os
import click
from .mlconjug import Conjugator
import json
import tomlkit
import yaml
import logging
from rich.pretty import pprint, Pretty
from rich.table import Table
from rich.columns import Columns
from rich.console import Console
import rich

@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.argument('verbs', nargs=-1)
@click.option('-l', '--language',
              default='fr',
              help=_("The language for the conjugation pipeline."
                     " The values can be 'fr', 'en', 'es', 'it', 'pt' or 'ro'."
                     " The default value is fr."),
              type=click.STRING)
@click.option('-o', '--output',
              default=None,
              help=_("Path of the filename for storing the conjugation tables."),
              type=click.STRING)
@click.option('-s', '--subject',
              default='abbrev',
              help=_("The subject format type for the conjugated forms."
                     " The values can be 'abbrev' or 'pronoun'. The default value is 'abbrev'."),
              type=click.STRING)
@click.option('-f', '--file_format',
              default='json',
              help=("The output format for storing the conjugation tables."
              " The values can be 'json', 'csv'. The default value is 'json'."),
              type=click.STRING)
@click.option('-c', '--config',
              default=None,
              help=("Path of the configuration file for specifying language, subject, output file name and format, "
              "as well as theme settings for the conjugation table columns. Supported file formats: toml, yaml"),
              type=click.Path(exists=True, dir_okay=False, resolve_path=True))
def main(verbs, language, output, subject, file_format, config):
    """
    Examples of how to use mlconjug3 from the terminal

    To conjugate a verb in English, abbreviated subject format :
    $ mlconjug3 -l en -s abbrev 'have'

    To conjugate multiple verbs in French, full subject format :
    $ mlconjug3 -l fr -s pronoun 'aimer' 'être' 'aller'

    To conjugate a verb in Spanish, full subject format and save the conjugation table in a json file:
    $ mlconjug3 -l es -s pronoun -f json 'hablar' -o 'conjugation_table.json'

    To conjugate multiple verbs in Italian, abbreviated subject format and save the conjugation table in a csv file:
    $ mlconjug3 -l it -s abbrev -f csv 'parlare' 'avere' 'essere' -o 'conjugation_table.csv'

    Examples of how to use mlconjug3 from the terminal with a config file:

    To use a config file in your home directory:
    $ mlconjug3 -c

    To use a specific config file:
    $ mlconjug3 -c /path/to/config.toml

    To use a specific config file and override some of the settings:
    $ mlconjug3 -c /path/to/config.toml -l en -s pronoun -o conjugation_table.json -f csv
    """
    config_options = load_config(config)
    language = config_options.get('language', language)
    subject = config_options.get('subject', subject)
    output = config_options.get('output', output)
    file_format = config_options.get('file_format', file_format)
    theme_settings = config_options.get('theme', {})
    try:
        logger = logging.getLogger(__name__)
        console = Console()
        # create console handler and set level to debug
        console_handler = logging.StreamHandler(sys.stdout)
        error_handler = logging.StreamHandler(sys.stderr)
        console_handler.setLevel(logging.INFO)
        error_handler.setLevel(logging.ERROR)
        logger.addHandler(console_handler)
        logger.addHandler(error_handler)
        logger.setLevel(logging.INFO)

        conjugator = Conjugator(language)
        conjugations = {}
        missing = []
        if len(verbs) == 1:
            result = conjugator.conjugate(verbs[0], subject)
            if result:
                conjugations[verbs[0]] = result.conjug_info
            else:
                missing.append(verbs[0])
        else:
            results = conjugator.conjugate(verbs, subject)
            conjugations = {verb.name: verb.conjug_info for verb in  results if verb}
            missing = [verb for verb, result in zip(verbs, results) if not result]
        
        for verb, conjugation in conjugations.items():
            table = Table(title=f"Conjugation table for '{verb.capitalize()}'", show_header=True, header_style=theme_settings.get("header_style", "bold #0D47A1"))
            table.add_column("Mood", style=theme_settings.get("mood_style", "bold #F9A825"))
            table.add_column("Tense", style=theme_settings.get("tense_style", "bold bright_magenta"))
            table.add_column("Person", style=theme_settings.get("person_style", "bold cyan"))
            table.add_column("Conjugation", style=theme_settings.get("conjugation_style", "bold #4CAF50"))

            for mood, tenses in conjugation.items():
                for tense, persons in tenses.items():
                    if isinstance(persons, dict):
                        for person, form in persons.items():
                            table.add_row(mood.capitalize(), tense.capitalize(), person, form)
                    else:
                        table.add_row(mood.capitalize(), tense.capitalize(), '', persons)
                    table.add_section()
                table.add_section()
            console.print(table)

        if missing:
            for verb in missing:
                console.print(f"The verb '{verb}' could not be conjugated.")
        
        if output:
            if file_format == 'json':
                with open(output, 'w') as outfile:
                    json.dump(conjugations, outfile)
            elif file_format == 'csv':
                with open(output, 'w') as outfile:
                    writer = csv.writer(outfile)
                    writer.writerow(["Verb", "Mood", "Tense", "Person", "Conjugation"])
                    for verb, conjugation in conjugations.items():
                        for mood, tenses in conjugation.items():
                            for tense, persons in tenses.items():
                                if isinstance(persons, dict):
                                    for person, form in persons.items():
                                        writer.writerow([verb, mood, tense, person, form])
                                else:
                                    writer.writerow([verb, mood, tense, '', persons])
            else:
                raise ValueError("Invalid output format. Please choose 'json' or 'csv'.")
    except Exception as e:
        logging.error("An error occurred: {}".format(e))
        if output:
            click.echo("Conjugations not saved. Please check the output file path and permissions.")
        else:
            click.echo("Conjugations not displayed. Please check the input verbs and language.")
        sys.exit(1)


def load_config(config):
    """
    Loads the config file in the given format (toml or yaml).
    If no config file is specified, looks for a default file named /mlconjug3/config.toml or /mlconjug3/config.yaml' in the user’s home directory.
    :param config: The path to the config file.
    :type config: str
    :return: A dictionary containing the configuration options.
    :rtype: dict
    """
    if not config:
        home = os.path.expanduser("~")
        config = os.path.join(home, 'mlconjug3/config.toml')
        if not os.path.isfile(config):
            config = os.path.join(home, 'mlconjug3/config.yaml')
            if not os.path.isfile(config):
                return {}
    config_options = {}
    if config.endswith('.toml'):
        with open(config, 'r') as config_file:
            config_options = tomlkit.loads(config_file.read())
    elif config.endswith('.yaml') or config.endswith('.yml'):
        with open(config, 'r') as config_file:
            config_options = yaml.load(config_file, Loader=yaml.FullLoader)
    return config_options
    
if __name__ == "__main__":
    main()

      
