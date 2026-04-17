from importlib import resources

from yaml import load

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

import yaml


RESOURCE_PACKAGE = "mlconjug3"


def _load_yaml_resource(package: str, resource: str):
    """
    Load a YAML file from package resources in a zip-safe way.
    """
    with resources.files(package).joinpath(resource).open("r", encoding="utf-8") as stream:
        return load(stream, Loader=Loader)


# Load config.yaml safely
constants = _load_yaml_resource(RESOURCE_PACKAGE, "config/config.yaml")

ABBREVS = constants["ABBREVS"]
ALPHABET = constants["ALPHABET"]
AUXILIARIES = constants["AUXILIARIES"]
CONJUGATIONS_RESOURCE_PATH = constants["CONJUGATIONS_RESOURCE_PATH"]
GENDER = constants["GENDER"]
IMPERATIVE_PRONOUNS = constants["IMPERATIVE_PRONOUNS"]
LANGUAGE_FULL = constants["LANGUAGE_FULL"]
LANGUAGES = constants["LANGUAGES"]
NEGATION = constants["NEGATION"]
PRE_TRAINED_MODEL_PATH = constants["PRE_TRAINED_MODEL_PATH"]
PRONOUNS = constants["PRONOUNS"]
SUPPORTED_LANGUAGES = constants["SUPPORTED_LANGUAGES"]

# ⚠️ Do NOT overwrite RESOURCE_PACKAGE blindly unless you really intend to
CONFIG_RESOURCE_PACKAGE = constants.get("RESOURCE_PACKAGE", RESOURCE_PACKAGE)

TRANSLATED_LANGUAGES = constants["TRANSLATED_LANGUAGES"]

# 👇 Export a Traversable instead of a string path
TRANSLATIONS_RESOURCE = resources.files(CONFIG_RESOURCE_PACKAGE).joinpath("locale")

VERBS_RESOURCE_PATH = constants["VERBS_RESOURCE_PATH"]


if __name__ == "__main__":
    pass
