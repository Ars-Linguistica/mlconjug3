# -*- coding: utf-8 -*-

"""
MLConjug.

A Python library to conjugate verbs of in French, English, Spanish, Italian, Portuguese and Romanian (mores soon) using Machine Learning techniques.
Any verb in one of the supported language can be conjugated as the module contains a Machine Learning pipeline of how the verbs behave.
Even completely new or made-up verbs can be successfully conjugated in this manner.
The supplied pre-trained models are composed of:

- a binary feature extractor,
- a feature selector using Linear Support Vector Classification,
- a classifier using Stochastic Gradient Descent.

MLConjug uses scikit-learn to implement the Machine Learning algorithms.
Users of the library can use any compatible classifiers from scikit-learn to modify and retrain the pipeline.

Usage example:
    $ mlconjug manger

    $ mlconjug bring -l en

    $ mlconjug gallofar --language es

"""

__author__ = """SekouD"""
__email__ = 'sekoud.python@gmail.com'
__version__ = '3.4.0'
__copyright__ = "Copyright (c) 2017, SekouD"
__credits__ = ("Pierre Sarrazin",)
__license__ = "MIT"
__maintainer__ = "SekouD"
__status__ = "Production"

from .mlconjug import *
from .PyVerbiste import *

from sklearn.feature_selection import SelectFromModel
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import LinearSVC
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline

import pkg_resources
import platform
from locale import windows_locale, getdefaultlocale
import gettext
import inspect

# Sets up the automatic translation of annotated strings displayed to the user.
_RESOURCE_PACKAGE = __name__
_TRANSLATIONS_PATH = pkg_resources.resource_filename(_RESOURCE_PACKAGE, 'locale')

_SUPPORTED_LANGUAGES = ('default', 'en', 'es', 'fr', 'it', 'pt', 'ro')
_TRANSLATED_LANGUAGES = _SUPPORTED_LANGUAGES[2:]


def _get_user_locale():
    """
    | Gets the user locale to set the user interface language language.
    | The default is set to english if the user's system locale is not one of the translated languages.

    :return: string.
        The user locale.

    """
    if 'Windows' in platform.system():
        import ctypes
        windll = ctypes.windll.kernel32
        default_locale = windows_locale[windll.GetUserDefaultUILanguage()]
    else:
        default_locale = getdefaultlocale()
    if default_locale:
        if isinstance(default_locale, tuple):
            user_locale = [0][:2]
        else:
            user_locale = default_locale[:2]
    else:
        user_locale = 'en'
    return user_locale


def _getdoc(object):
    """
    Translates the docstrings of the objects defined in the packeage in the supported languages.

    :param object:
    :return: string.
        The translated version of the object's docstring.
    """
    try:
        doc = object.__doc__
    except AttributeError:
        return None
    if not isinstance(doc, str):
        return None
    return inspect.cleandoc(_(doc))


_user_locale = _get_user_locale()

if _user_locale in _TRANSLATED_LANGUAGES:
    _MLCONJUG_TRANSLATIONS = gettext.translation(domain='mlconjug',
                                                localedir=_TRANSLATIONS_PATH,
                                                languages=[_user_locale], fallback=True, codeset='UTF-8')
else:
    _MLCONJUG_TRANSLATIONS = gettext.NullTranslations()

_MLCONJUG_TRANSLATIONS.install()


# Replaces the getdoc method
inspect.getdoc = _getdoc
