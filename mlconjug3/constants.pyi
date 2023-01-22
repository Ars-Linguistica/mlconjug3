from lib2to3.pgen2.token import OP
from typing import Sequence, Mapping, Dict, Tuple, Optional, Union, Set, TextIO

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
