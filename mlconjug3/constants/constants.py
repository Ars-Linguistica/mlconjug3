import pkg_resources

import tomlkit

with open("../config/constants.yaml", "r") as file:
    config = tomlkit.loads(file.read())

ABBREVS = tuple(config["ABBREVS"])
ALPHABET = config["ALPHABET"]
AUXILIARIES = config["AUXILIARIES"]
CONJUGATIONS_RESOURCE_PATH = config["CONJUGATIONS_RESOURCE_PATH"]
GENDER = config["GENDER"]
IMPERATIVE_PRONOUNS = config["IMPERATIVE_PRONOUNS"]
LANGUAGE_FULL = config["LANGUAGE_FULL"]
LANGUAGES = tuple(config["LANGUAGES"])
NEGATION = config["NEGATION"]
PRE_TRAINED_MODEL_PATH = config["PRE_TRAINED_MODEL_PATH"]
PRONOUNS = config["PRONOUNS"]
RESOURCE_PACKAGE = config["RESOURCE_PACKAGE"]
SUPPORTED_LANGUAGES = tuple(config["SUPPORTED_LANGUAGES"])
TRANSLATED_LANGUAGES = tuple(config["TRANSLATED_LANGUAGES"])
TRANSLATIONS_PATH = config["TRANSLATIONS_PATH"]
VERBS_RESOURCE_PATH = config["VERBS_RESOURCE_PATH"]


if __name__ == "__main__":
    pass
