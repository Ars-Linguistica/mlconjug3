# -*- coding: utf-8 -*-

"""
MLConjug3.
(unchanged docstring)
"""

__author__ = "Sekou Diao, Ars Linguistica"
__email__ = "diao.sekou.nlp@gmail.com"
__version__ = "3.11.0"
__copyright__ = "Copyright (c) 2023, Ars Linguistica"
__credits__ = (
    "Sekou Diao",
    "Pierre Sarrazin",
)
__license__ = "MIT"
__maintainer__ = "Ars-Linguistica"
__status__ = "Production"

from .constants import *
from .constants.constants import TRANSLATIONS_RESOURCE
from .mlconjug import *
from .PyVerbiste import *

from sklearn.feature_selection import SelectFromModel
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import LinearSVC
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline

import platform
from locale import windows_locale, getlocale
import gettext
import inspect
from importlib import resources


def _get_user_locale():
    """
    Gets the user locale to set the user interface language.
    Defaults to English if unsupported.
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
    Translates the docstrings of the objects defined in the package.
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
    Load gettext translations in a fully zip-safe way.
    """
    if _user_locale not in TRANSLATED_LANGUAGES:
        return gettext.NullTranslations()

    try:
        # Materialize locale directory safely (even from zip)
        with resources.as_file(TRANSLATIONS_RESOURCE) as locale_path:
            return gettext.translation(
                domain="mlconjug3",
                localedir=str(locale_path),
                languages=[_user_locale],
                fallback=True,
            )
    except Exception:
        return gettext.NullTranslations()


MLCONJUG_TRANSLATIONS = _get_translations()
MLCONJUG_TRANSLATIONS.install()

# Replace the default getdoc method
inspect.getdoc = _getdoc
