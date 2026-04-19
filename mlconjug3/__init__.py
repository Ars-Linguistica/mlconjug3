# -*- coding: utf-8 -*-

"""
mlconjug3
=========

Main package initializer for mlconjug3.

This module:
- Defines package metadata
- Initializes translation system
- Exposes core ML and rule-based conjugation components
- Overrides docstring handling for localization support
"""

__author__ = "Sekou Diao, Ars Linguistica"
__email__ = "diao.sekou.nlp@gmail.com"
__version__ = "4.0.0"
__copyright__ = "Copyright (c) 2023, Ars Linguistica"
__credits__ = (
    "Sekou Diao",
    "Pierre Sarrazin",
)
__license__ = "MIT"
__maintainer__ = "Ars-Linguistica"
__status__ = "Production"


# -----------------------------
# Public API imports
# -----------------------------
from .constants import *
from .constants.constants import TRANSLATIONS_RESOURCE
from .mlconjug import *
from .PyVerbiste import *
from .utils.model_trainer import ConjugatorTrainer

from sklearn.feature_selection import SelectFromModel
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import LinearSVC
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline

import platform
import inspect
import gettext
from locale import windows_locale, getlocale
from importlib import resources


# Bind translation function explicitly for Sphinx safety
_ = gettext.gettext


def _get_user_locale():
    """
    Detect the user's system locale.

    Returns
    -------
    str
        Two-letter ISO language code (e.g., 'en', 'fr').

    Notes
    -----
    - On Windows, uses system UI language via ctypes.
    - On Unix systems, uses locale.getlocale().
    - Defaults to 'en' if detection fails.
    """
    if "Windows" in platform.system():
        import ctypes

        windll = ctypes.windll.kernel32
        default_locale = windows_locale.get(windll.GetUserDefaultUILanguage())
    else:
        default_locale = getlocale()

    if default_locale:
        if isinstance(default_locale, tuple):
            user_locale = default_locale[0][:2] if default_locale[0] else "en"
        else:
            user_locale = default_locale[:2]
    else:
        user_locale = "en"

    return user_locale


def _getdoc(obj):
    """
    Retrieve and localize docstrings for Sphinx compatibility.

    Parameters
    ----------
    obj : object
        Python object with a docstring.

    Returns
    -------
    str or None
        Cleaned and translated docstring, or None if unavailable.
    """
    try:
        doc = obj.__doc__
    except AttributeError:
        return None

    if not isinstance(doc, str):
        return None

    return inspect.cleandoc(_(doc))


_user_locale = _get_user_locale()


def _get_translations():
    """
    Load gettext translation catalog safely.

    Returns
    -------
    gettext.NullTranslations or gettext.GNUTranslations
        Translation object for the detected locale.

    Notes
    -----
    - Fully zip-safe via importlib.resources
    - Falls back to NullTranslations if locale unsupported or missing
    """
    if _user_locale not in TRANSLATED_LANGUAGES:
        return gettext.NullTranslations()

    try:
        with resources.as_file(TRANSLATIONS_RESOURCE) as locale_path:
            return gettext.translation(
                domain="mlconjug3",
                localedir=str(locale_path),
                languages=[_user_locale],
                fallback=True,
            )
    except Exception:
        return gettext.NullTranslations()


# -----------------------------
# Initialize translations
# -----------------------------
MLCONJUG_TRANSLATIONS = _get_translations()
MLCONJUG_TRANSLATIONS.install()

# Override default docstring retrieval for localization
inspect.getdoc = _getdoc
