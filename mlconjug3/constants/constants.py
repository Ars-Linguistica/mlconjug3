"""
Constants module for mlconjug3.

This module loads and exposes configuration constants used throughout
the library, including language metadata, morphological rules, and
resource paths.

All constants are loaded from a YAML configuration file bundled with
the package resources.
"""

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
    Load a YAML resource file from package data in a zip-safe manner.

    This function ensures compatibility with installed packages,
    including zip-safe environments (e.g., wheels, zip imports).

    Parameters
    ----------
    package : str
        Name of the Python package containing the resource.
    resource : str
        Relative path to the YAML file inside the package.

    Returns
    -------
    dict
        Parsed YAML content as a Python dictionary.
    """
    with resources.files(package).joinpath(resource).open(
        "r", encoding="utf-8"
    ) as stream:
        return load(stream, Loader=Loader)


# Load configuration constants
constants = _load_yaml_resource(RESOURCE_PACKAGE, "config/config.yaml")

# ---------------------------
# CORE MORPHOLOGICAL DATA
# ---------------------------
ABBREVS = constants["ABBREVS"]
ALPHABET = constants["ALPHABET"]
AUXILIARIES = constants["AUXILIARIES"]

# ---------------------------
# LANGUAGE & STRUCTURE DATA
# ---------------------------
CONJUGATIONS_RESOURCE_PATH = constants["CONJUGATIONS_RESOURCE_PATH"]
GENDER = constants["GENDER"]
IMPERATIVE_PRONOUNS = constants["IMPERATIVE_PRONOUNS"]
LANGUAGE_FULL = constants["LANGUAGE_FULL"]
LANGUAGES = constants["LANGUAGES"]
NEGATION = constants["NEGATION"]

# ---------------------------
# MODEL & RESOURCE PATHS
# ---------------------------
PRE_TRAINED_MODEL_PATH = constants["PRE_TRAINED_MODEL_PATH"]
VERBS_RESOURCE_PATH = constants["VERBS_RESOURCE_PATH"]

# ---------------------------
# LANGUAGE SUPPORT
# ---------------------------
PRONOUNS = constants["PRONOUNS"]
SUPPORTED_LANGUAGES = constants["SUPPORTED_LANGUAGES"]
TRANSLATED_LANGUAGES = constants["TRANSLATED_LANGUAGES"]

# Optional override for translation resources
CONFIG_RESOURCE_PACKAGE = constants.get(
    "RESOURCE_PACKAGE", RESOURCE_PACKAGE
)

# Export translation resource directory as Traversable object
TRANSLATIONS_RESOURCE = resources.files(CONFIG_RESOURCE_PACKAGE).joinpath(
    "locale"
)


if __name__ == "__main__":
    pass
