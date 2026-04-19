# Stubs for mlconjug3.PyVerbiste (Python 3)

from typing import Sequence, Mapping, Dict, Tuple, Optional, Union, Set, TextIO
from collections import OrderedDict
from xml.etree.ElementTree import Element
import os

from mlconjug3.conjug_manager import ConjugManager
from mlconjug3.constants import *

__author__: str
__author_email__: str


# ---------------------------
# Shared type aliases
# ---------------------------

_VerbsDict = Mapping[str, Mapping[str, str]]
_Tense = Mapping[str, Sequence[Optional[Tuple[int, str]]]]
_Mood = Dict[str, Union[str, _Tense]]
_ConjugInfo = Mapping[str, _Mood]
_Conjugations = Mapping[str, _ConjugInfo]

# ✅ FIX: must match base class exactly
_PathLike = Union[str, os.PathLike[str], TextIO]


class Verbiste(ConjugManager):
    """
    Stub for Verbiste class extending ConjugManager.
    """

    def _load_verbs(self, verbs_file: _PathLike) -> None: ...

    def _parse_verbs(self, file: _PathLike) -> Mapping[str, Mapping[str, str]]: ...

    def _load_conjugations(self, conjugations_file: _PathLike) -> None: ...

    def _parse_conjugations(self, file: _PathLike) -> _Conjugations: ...

    def _load_tense(
        self, tense: Element
    ) -> Union[str, None, Sequence[Tuple[int, Optional[str]]]]: ...
