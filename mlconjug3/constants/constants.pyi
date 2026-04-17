from lib2to3.pgen2.token import OP
from typing import Sequence, Mapping, Dict, Tuple, Optional, Union, Set, TextIO, Type
import gettext
from mlconjug3.verbs import Verb

RESOURCE_PACKAGE: str = __name__
LANGUAGES: Tuple[str, ...]
VERBS_RESOURCE_PATH: Mapping[str, str]
CONJUGATIONS_RESOURCE_PATH: Mapping[str, str]
ABBREVS: Tuple[str, ...]
PRONOUNS: Mapping[str, Mapping[str, Tuple[str]]]
IMPERATIVE_PRONOUNS: Mapping[str, Optional[Mapping[str, Tuple[str]]]]
GENDER: Mapping[str, Optional[Mapping[str, Tuple[str]]]]
NEGATION: Mapping[str, str]
LANGUAGE_FULL: Mapping[str, str]
VERBS: Mapping[str, Type[Verb]]
PRE_TRAINED_MODEL_PATH: Mapping[str, str]
TRANSLATIONS_PATH: str
SUPPORTED_LANGUAGES: Tuple[str, ...]
TRANSLATED_LANGUAGES: Tuple[str]
MLCONJUG_TRANSLATIONS: Union[gettext.GNUTranslations, gettext.NullTranslations]
