# -*- coding: utf-8 -*-

"""Console script for mlconjug."""

import click
from .mlconjug import Conjugator
from pprint import pprint


@click.command()
@click.argument('verb')
@click.option('-l', '--language',
              default='fr',
              help=_("The language for the conjugation pipeline. The values can be fr, en, es, it, pt or ro. The default value is fr."),
              type=click.STRING)
def main(verb, language):
    """Console script for mlconjug."""
    conjugator = Conjugator(language)
    result = conjugator.conjugate(verb)
    pprint(result.conjug_info)
    return


if __name__ == "__main__":
    main()
