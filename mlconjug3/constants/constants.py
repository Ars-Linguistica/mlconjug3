import pkg_resources

import os

from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


import yaml

RESOURCE_PACKAGE = 'mlconjug3'

config_file = pkg_resources.resource_filename(RESOURCE_PACKAGE, 'config/config.yaml')
with open(config_file, 'r') as stream:
    try:
        constants = load(stream, Loader=Loader)
        ABBREVS = constants['ABBREVS']
        ALPHABET = constants['ALPHABET']
        AUXILIARIES = constants['AUXILIARIES']
        CONJUGATIONS_RESOURCE_PATH = constants['CONJUGATIONS_RESOURCE_PATH']
        GENDER = constants['GENDER']
        IMPERATIVE_PRONOUNS = constants['IMPERATIVE_PRONOUNS']
        LANGUAGE_FULL = constants['LANGUAGE_FULL']
        LANGUAGES = constants['LANGUAGES']
        NEGATION = constants['NEGATION']
        PRE_TRAINED_MODEL_PATH = constants['PRE_TRAINED_MODEL_PATH']
        PRONOUNS = constants['PRONOUNS']
        SUPPORTED_LANGUAGES = constants['SUPPORTED_LANGUAGES']
        RESOURCE_PACKAGE = constants['RESOURCE_PACKAGE']
        TRANSLATED_LANGUAGES = constants['TRANSLATED_LANGUAGES']
        TRANSLATIONS_PATH = pkg_resources.resource_filename(RESOURCE_PACKAGE, 'locale')
        VERBS_RESOURCE_PATH = constants['VERBS_RESOURCE_PATH']
    except yaml.YAMLError as exc:
        print(exc)

if __name__ == "__main__":
    pass
