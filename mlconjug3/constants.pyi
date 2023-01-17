from typing import Dict, Tuple

_LANGUAGES: Tuple[str, ...]
_TRANSLATIONS_PATH: str
_SUPPORTED_LANGUAGES: Tuple[str, ...]
_TRANSLATED_LANGUAGES: Tuple[str, ...]
_LANGUAGE_FULL: Dict[str, str]
_VERBS: Dict[str, Type[Verb]]
_PRE_TRAINED_MODEL_PATH: Dict[str, str]
_ALPHABET: Dict[str, Dict[str, str]]
_VERBS_RESOURCE_PATH: Dict[str, str]
_CONJUGATIONS_RESOURCE_PATH: Dict[str, str]
_ABBREVS: Tuple[str, str, str, str, str, str]
_PRONOUNS: Dict[str, Dict[str, Union[Tuple[str, str, str, str, str, str], Tuple[str, str, str, str, str, str]]]]
_IMPERATIVE_PRONOUNS: Dict[str, Union[None, Dict[str, Union[None, Tuple[str, str, str, str, str]]]]]
_AUXILIARIES: Dict[str, Union[None, str]]
_GENDER: Dict[str, Union[None, Dict[str, Union[None, Tuple[str, str, str, str]]]]]
_NEGATION: Dict[str, Union[None, str]]
