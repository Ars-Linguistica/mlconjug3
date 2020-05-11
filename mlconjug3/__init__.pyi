# Stubs for mlconjug3 (Python 3)


from .mlconjug import *
from .PyVerbiste import *
from typing import Text, Tuple, Any, Union
from logging import Logger
import gettext

__author__: Text
__email__: Text
__version__: Text
__copyright__: Text
__credits__: Tuple[Text]
__license__: Text
__maintainer__: Text
__status__: Text
SelectFromModel: Any
CountVectorizer: Any
LinearSVC: Any
SGDClassifier: Any
logger: Logger
_RESOURCE_PACKAGE: Text = __name__
_TRANSLATIONS_PATH: Text
_SUPPORTED_LANGUAGES: Tuple[Text, ...]
_TRANSLATED_LANGUAGES: Tuple[Text]
_MLCONJUG_TRANSLATIONS: Union[gettext.GNUTranslations, gettext.NullTranslations]
_user_locale: Text

def _get_user_locale() -> Text: ...

def _getdoc(obj: object) -> Text: ...
