# -*- coding: utf-8 -*-

"""Console script for mlconjug3."""

import click
from .mlconjug import Conjugator
import json
import logging
import sys


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
def main(verbs, language, output, subject):
    """
    MLConjug is a Python library to conjugate verbs of in French, English, Spanish, Italian, Portuguese and Romanian (mores soon) using Machine Learning techniques.
    Any verb in one of the supported language can be conjugated as the module contains a Machine Learning pipeline of how the verbs behave.
    Even completely new or made-up verbs can be successfully conjugated in this manner.
    The supplied pre-trained models are composed of:

    - a binary feature extractor,

    - a feature selector using Linear Support Vector Classification,

    - a classifier using Stochastic Gradient Descent.

    MLConjug uses scikit-learn to implement the Machine Learning algorithms.
    Users of the library can use any compatible classifiers from scikit-learn to modify and retrain the pipeline.

    Usage example:
        $ mlconjug3 manger

        $ mlconjug3 bring -l en

        $ mlconjug3 gallofar --language es

    """
    logger = logging.getLogger(__name__)

    # create console handler and set level to debug
    console_handler = logging.StreamHandler(sys.stdout)
    error_handler = logging.StreamHandler(sys.stderr)
    console_handler.setLevel(logging.INFO)
    error_handler.setLevel(logging.ERROR)
    logger.addHandler(console_handler)
    logger.addHandler(error_handler)
    logger.setLevel(logging.INFO)
    conjugator = Conjugator(language)
    results = {}
    for verb in verbs:
        result = conjugator.conjugate(verb, subject)
        results[verb] = result.conjug_info
    if output:
        with open(output, 'w', encoding='utf-8') as file:
            json.dump(results, file, ensure_ascii=False, indent=4)
            print('The conjugations have been succesfully saved to {0}.'.format(output))
    else:
        print(json.dumps(results, ensure_ascii=False, indent=4))
    # Use print(in CLI to prevent doubling of output.
    # logger.info(json.dumps(results, ensure_ascii=False, indent=4))
    return


if __name__ == "__main__":
    main()
