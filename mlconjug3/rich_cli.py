from rich.pretty import pprint
from rich.table import Table
from .mlconjug import Conjugator
import json
import logging
import sys
from rich import print

def setup_logging(logger):
    console_handler = logging.StreamHandler(sys.stdout)
    error_handler = logging.StreamHandler(sys.stderr)
    console_handler.setLevel(logging.INFO)
    error_handler.setLevel(logging.ERROR)
    logger.addHandler(console_handler)
    logger.addHandler(error_handler)
    logger.setLevel(logging.INFO)

def conjugate_verbs(verbs, language, subject):
    logger = logging.getLogger(__name__)
    conjugator = Conjugator(language)
    results = {}
    for verb in verbs:
        result = conjugator.conjugate(verb, subject)
        results[verb] = result.conjug_info
    return results

def write_conjugations_to_file(results, output):
    with open(output, 'w', encoding='utf-8') as file:
            json.dump(results, file, ensure_ascii=False, indent=4)
            print('The conjugations have been succesfully saved to {0}.'.format(output))

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
@click.option('-t', '--theme',
              default='light',
              help=_("Choose between different themes for the output."
                     " The values can be 'light' or 'dark'. The default value is 'light'."),
              type=click.STRING)
def main(verbs, language, output, subject, theme):
    """
    MLConjug is a Python library to conjugate verbs of in French, English, Spanish, Italian, Portuguese and Romanian (mores soon) using Machine Learning techniques.
    Any verb in one of the supported language can be conjugated as the module contains a Machine Learning pipeline of how the verbs behave.
    Even completely new or made-up verbs can be successfully conjugated in this manner.
    The supplied pre-trained models are composed of:
    a binary feature extractor,
    a feature selector using Linear Support Vector Classification,
    a classifier using Stochastic Gradient Descent.
    MLConjug uses scikit-learn to implement the Machine Learning algorithms.
    Users of the library can use any compatible classifiers from scikit-learn to modify and retrain the pipeline.
    Usage example:
    $ mlconjug3 manger
    $ mlconjug3 bring -l en

    $ mlconjug3 gallofar --language es
    """
    logger = logging.getLogger(__name__)
    console_handler = logging.StreamHandler(sys.stdout)
    error_handler = logging.StreamHandler(sys.stderr)
    console_handler.setLevel(logging.INFO)
    error_handler.setLevel(logging.ERROR)
    logger.addHandler(console_handler)
    logger.addHandler(error_handler)
    logger.setLevel(logging.INFO)
    if theme=="light":
        from rich import print
        print("Using light theme")
    elif theme=="dark":
        from rich import print
        print("Using dark theme")
    else:
        print("Invalid theme choice")
    if not verbs:
        print("Please provide at least one verb to conjugate.")
        return
    results = conjugate_verbs(verbs, language, subject)
    if output:
        write_conjugations_to_file(results, output)
    else:
        for verb in results:
            table = Table(show_header=True, header_style="bold red")
            table.add_column("Pronoun", style="dim", width=15)
            table.add_column("Conjugated Form", style="green", width=25)
            for pronoun, conjugation in results[verb].items():
                table.add_row(pronoun, conjugation)
            print(f"[bold yellow]Conjugation of the verb {verb}[/bold yellow]")
            print(table)


if name == 'main':
    main()

    
