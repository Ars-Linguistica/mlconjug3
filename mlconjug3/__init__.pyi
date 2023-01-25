# Stubs for mlconjug3 (Python 3)


from .mlconjug import *
from .PyVerbiste import *
from typing import Tuple, Any, Union
from logging import Logger
import gettext

__author__: str
__email__: str
__version__: str
__copyright__: str
__credits__: Tuple[str, ...]
__license__: str
__maintainer__: str
__status__: str
SelectFromModel: Any
CountVectorizer: Any
LinearSVC: Any
SGDClassifier: Any
Pipeline: Any
logger: Logger
_user_locale: str

def _get_user_locale() -> str: ...

def _getdoc(obj: object) -> str: ...
