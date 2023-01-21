# -*- coding: utf-8 -*-

"""Console script for mlconjug3."""

import sys
import click
from .mlconjug import Conjugator
import json
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
def main(verbs, language, output, subject, file_format):
    """
    MLConjug is a Python library to conjugate verbs of in French, English, Spanish, Italian, Portuguese and Romanian (mores soon) using Machine Learning techniques.
    Any verb in one of the supported language can be conjugated as the module contains a Machine Learning pipeline of how the verbs behave.
    Even completely new or made-up verbs can be successfully conjugated in this manner.
    The supplied pre-trained models are composed of: - a binary feature extractor,
    
    - a feature selector using Linear Support Vector Classification,
    
    - a classifier using Stochastic Gradient Descent.
    
    MLConjug uses scikit-learn to implement the Machine Learning algorithms.
    Users of the library can use any compatible classifiers from scikit-learn to modify and retrain the pipeline.
    
    Usage example:
        $ mlconjug3 -l en -s abbrev 'have' 'be' 'go'
        $ mlconjug3 -l fr -s pronoun 'aimer' 'être' 'aller'
    
    """
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
        for verb in verbs:
            conjugations[verb] = conjugator.conjugate(verb, subject).conjug_info
        
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Verb")
        table.add_column("Mood")
        table.add_column("Tense")
        table.add_column("Person")
        table.add_column("Conjugation")
        
        for verb, conjugation in conjugations.items():
            for mood, tenses in conjugation.items():
                for tense, persons in tenses.items():
                    for person in persons:
                        table.add_row(verb, mood, tense, person)
        
        console.print(table)
        if output:
            if file_format == 'json':
                with open(output, 'w') as outfile:
                    json.dump(conjugations, outfile)
            elif file_format == 'csv':
                pass # code to write to csv file
            else:
                raise ValueError("Invalid output format. Please choose 'json', 'csv' or 'pdf'.")
    except Exception as e:
        logging.error("An error occurred: {}".format(e))
        if output:
            click.echo("Conjugations not saved. Please check the output file path and permissions.")
        else:
            click.echo("Conjugations not displayed. Please check the input verbs and language.")
        sys.exit(1)
    
if __name__ == "__main__":
    main()

      
