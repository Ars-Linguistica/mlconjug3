# Stubs for mlconjug3.PyVerbiste (Python 3)

from lib2to3.pgen2.token import OP
from typing import Sequence, Mapping, Dict, Tuple, Optional, Union, Set, TextIO
from collections import OrderedDict
from xml.etree.ElementTree import Element
from .conjug_manager import ConjugManager

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


class Verbiste(ConjugManager):
    def _load_verbs(self,
                    verbs_file: _PathLike
                    ) -> None: ...

    def _parse_verbs(self,
                     file: _PathLike
                     ) -> Mapping[str,Mapping[str, str]]: ...

    def _load_conjugations(self,
                           conjugations_file: _PathLike
                           ) -> None: ...

    def _parse_conjugations(self,
                            file: _PathLike
                            ) -> _Conjugations: ...

    def _load_tense(self,
                    tense: Element
                    ) -> Union[str, None, Sequence[Tuple[int, Optional[str]]]]: ...
