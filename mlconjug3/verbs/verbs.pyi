# Stubs for mlconjug3.verbs.py (Python 3)

from lib2to3.pgen2.token import OP
from typing import Sequence, Mapping, Dict, Tuple, Optional, Union, Set, TextIO
from collections import OrderedDict
from xml.etree.ElementTree import Element

__author__: str
__author_email__: str
_RESOURCE_PACKAGE: str = __name__
_LANGUAGES: Tuple[str, ...]
_VERBS_RESOURCE_PATH: Mapping[str, str]
_CONJUGATIONS_RESOURCE_PATH: Mapping[str, str]
_ABBREVS: Tuple[str, ...]
_PRONOUNS: Mapping[str, Mapping[str, Tuple[str]]]
_IMPERATIVE_PRONOUNS: Mapping[str, Optional[Mapping[str, Tuple[str]]]]
_GENDER: Mapping[str, Optional[Mapping[str, Tuple[str]]]]
_NEGATION: Mapping[str, str]

# Declare Complex types for clarity.
_VerbsDict = Mapping[str, Mapping[str, str]]
_Tense = Mapping[str, Sequence[Optional[Tuple[int,str]]]]
_Mood = Dict[str, Union[str, _Tense]]
_ConjugInfo = Mapping[str, _Mood]
_Conjugations = Mapping[str, _ConjugInfo]
_PathLike = Union[str, TextIO]


class VerbInfo:
    __slots__: Tuple[str] = ...
    infinitive: str = ...
    root: str = ...
    template: str = ...
    def __init__(self,
                 infinitive: str,
                 root: str,
                 template: str
                 ) -> None: ...

    def __repr__(self) -> str: ...

    def __eq__(self,
               other: object
               ) -> bool: ...


class Verb:
    __slots__: Tuple[str] = ...
    language: str = ...
    name: str = ...
    verb_info: VerbInfo = ...
    conjug_info: _ConjugInfo = ...
    full_forms: _ConjugInfo = ...
    subject: str = ...
    predicted: bool = ...
    confidence_score: Optional[float] = ...
    def __init__(self,
                 verb_info: VerbInfo,
                 conjug_info: _ConjugInfo,
                 subject: str = ...,
                 predicted: bool = ...
                 ) -> None: ...

    def __repr__(self) -> str: ...

    def _load_conjug(self, subject: str) -> None: ...

    def iterate(self) -> Sequence[Union[Tuple[str,str,str],Tuple[str,str,str,str]]]: ...

    def conjugate_person(self,
                         key: str,
                         persons_dict: Mapping[str, str],
                         term: str
                         ) -> None: ...


class VerbFr(Verb):
    def _load_conjug(self, subject: str) -> None: ...


class VerbEn(Verb):
    def _load_conjug(self, subject: str) -> None: ...


class VerbEs(Verb):
    def _load_conjug(self, subject: str) -> None: ...


class VerbIt(Verb):
    def _load_conjug(self, subject: str) -> None: ...


class VerbPt(Verb):
    def _load_conjug(self, subject: str) -> None: ...


class VerbRo(Verb):
    def _load_conjug(self, subject: str) -> None: ...
      

