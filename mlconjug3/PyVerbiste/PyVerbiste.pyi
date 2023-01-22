# Stubs for mlconjug3.PyVerbiste (Python 3)

from lib2to3.pgen2.token import OP
from typing import Sequence, Mapping, Dict, Tuple, Optional, Union, Set, TextIO
from collections import OrderedDict
from xml.etree.ElementTree import Element
from mlconjug3.conjug_manager import ConjugManager
from mlconjug3.constants import *

__author__: str
__author_email__: str

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
