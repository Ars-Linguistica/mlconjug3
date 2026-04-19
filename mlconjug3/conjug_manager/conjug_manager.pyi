"""
Type stubs for mlconjug3.conjug_manager.ConjugManager
"""

from typing import (
    Sequence,
    Mapping,
    Dict,
    Tuple,
    Optional,
    Union,
    Set,
    TextIO,
    Any,
)
from collections import OrderedDict
import os

from mlconjug3.verbs import VerbInfo

__author__: str
__author_email__: str
_RESOURCE_PACKAGE: str
_LANGUAGES: Tuple[str, ...]
_VERBS_RESOURCE_PATH: Mapping[str, str]
_CONJUGATIONS_RESOURCE_PATH: Mapping[str, str]
_ABBREVS: Tuple[str, ...]
_PRONOUNS: Mapping[str, Mapping[str, Tuple[str]]]
_IMPERATIVE_PRONOUNS: Mapping[str, Optional[Mapping[str, Tuple[str]]]]
_GENDER: Mapping[str, Optional[Mapping[str, Tuple[str]]]]
_NEGATION: Mapping[str, str]

_VerbsDict = Mapping[str, Mapping[str, str]]
_Tense = Mapping[str, Sequence[Optional[Tuple[int, str]]]]
_Mood = Dict[str, Union[str, _Tense]]
_ConjugInfo = Mapping[str, _Mood]
_Conjugations = Mapping[str, _ConjugInfo]

_PathLike = Union[str, os.PathLike[str], TextIO]


class ConjugManager:
    """
    Handles verb and conjugation resources.
    """

    language: str
    verbs: Mapping[str, Mapping[str, str]]
    conjugations: _Conjugations
    _allowed_endings: Set[str]
    templates: Sequence[str]

    def __init__(self, language: str = ...) -> None: ...

    def __repr__(self) -> str: ...

    def _load_verbs(self, verbs_file: _PathLike) -> None: ...

    def _load_conjugations(self, conjugations_file: _PathLike) -> None: ...

    def _detect_allowed_endings(self) -> Set[str]: ...

    def is_valid_verb(self, verb: str) -> bool: ...

    def get_verb_info(self, verb: str) -> Optional[VerbInfo]: ...

    def get_conjug_info(self, template: str) -> Optional[_ConjugInfo]: ...

    def _load_cache(self, file: str) -> Optional[Any]: ...
