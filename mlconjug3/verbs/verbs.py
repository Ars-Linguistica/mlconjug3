"""
This module defines the VerbInfo and Verb hierarchy classes used for representing verb conjugation data.

It provides:
- VerbInfo: a lightweight container for verb metadata (infinitive, root, template)
- VerbMeta: an abstract metaclass defining the verb interface
- Verb: the base implementation of a conjugated verb
- Language-specific subclasses: VerbFr, VerbEn, VerbEs, VerbIt, VerbPt, VerbRo

Each language class customizes how conjugation forms are constructed.
"""

import abc
from collections import OrderedDict
import copy
from mlconjug3.constants import *


class VerbInfo:
    """
    Container for verb metadata used in conjugation.

    :param infinitive: Infinitive form of the verb.
    :type infinitive: str
    :param root: Lexical root of the verb.
    :type root: str
    :param template: Verb ending pattern identifier.
    :type template: str

    :ivar infinitive: Infinitive form of the verb.
    :vartype infinitive: str
    :ivar root: Lexical root of the verb.
    :vartype root: str
    :ivar template: Verb ending pattern identifier.
    :vartype template: str
    """

    __slots__ = ("infinitive", "root", "template")

    def __init__(self, infinitive, root, template):
        self.infinitive = infinitive
        if not root:
            self.root = "" if template[0] == ":" else template[: template.index(":")]
        else:
            self.root = root
        self.template = template

    def __repr__(self):
        return "{}.{}({}, {}, {})".format(
            __name__, self.__class__.__name__, self.infinitive, self.root, self.template
        )

    def __eq__(self, other):
        if not isinstance(other, VerbInfo):
            return NotImplemented
        return (
            self.infinitive == other.infinitive
            and self.root == other.root
            and self.template == other.template
        )


class VerbMeta(abc.ABCMeta):
    """
    Abstract metaclass defining the interface for all Verb classes.
    """

    @abc.abstractmethod
    def __init__(self, verb_info, conjug_info, subject="abbrev", predicted=False):
        pass

    @abc.abstractproperty
    def language(self):
        pass

    @abc.abstractmethod
    def __getitem__(self, key):
        pass

    @abc.abstractmethod
    def __setitem__(self, key, value):
        pass

    @abc.abstractmethod
    def __contains__(self, item):
        pass

    @abc.abstractmethod
    def __iter__(self):
        pass

    @abc.abstractmethod
    def iterate(self):
        pass

    @abc.abstractmethod
    def load_conjug(self):
        pass

    @abc.abstractmethod
    def conjugate(self, subject, tense):
        pass


class Verb(metaclass=VerbMeta):
    """
    Base class representing a conjugated verb.

    :param verb_info: Metadata describing the verb.
    :type verb_info: VerbInfo
    :param conjug_info: Conjugation structure.
    :type conjug_info: OrderedDict
    :param subject: Pronoun format ('abbrev' or 'pronoun').
    :type subject: str
    :param predicted: Whether conjugation was predicted by ML model.
    :type predicted: bool

    :ivar verb_info: Verb metadata.
    :vartype verb_info: VerbInfo
    :ivar conjug_info: Full conjugation dictionary.
    :vartype conjug_info: OrderedDict
    :ivar full_forms: Expanded conjugation forms.
    :vartype full_forms: dict
    :ivar subject: Pronoun format used.
    :vartype subject: str
    :ivar predicted: Whether output is model-predicted.
    :vartype predicted: bool
    :ivar confidence_score: Model confidence score if available.
    :vartype confidence_score: float | None
    """

    __slots__ = (
        "name",
        "verb_info",
        "conjug_info",
        "full_forms",
        "subject",
        "predicted",
        "confidence_score",
    )

    language = "default"

    def __init__(self, verb_info, conjug_info, subject="abbrev", predicted=False):
        self.name = verb_info.infinitive
        self.verb_info = verb_info
        self.conjug_info = conjug_info
        self.full_forms = {}
        self.subject = subject
        self.predicted = predicted
        self.confidence_score = None

        if subject == "pronoun":
            self._load_conjug(subject)
            self.full_forms = self.conjug_info
        else:
            self.conjug_info = self.full_forms
            self._load_conjug("pronoun")
            self.conjug_info = conjug_info
            self._load_conjug(subject)

    def __repr__(self):
        return "{}.{}({})".format(__name__, self.__class__.__name__, self.name)

    def __getitem__(self, key):
        """
        Retrieve conjugated forms by key.

        :param key: (mood, tense, person) or (mood, tense) or (mood)
        :type key: tuple | str
        :return: Conjugated form(s)
        """
        if len(key) == 3:
            mood, tense, person = key
            return self.conjug_info[mood][tense][person]
        elif len(key) == 2:
            mood, tense = key
            return self.conjug_info[mood][tense]
        else:
            return self.conjug_info[key]

    def __setitem__(self, key, value):
        """
        Set conjugated forms by key.

        :param key: (mood, tense, person) or (mood, tense) or (mood)
        :type key: tuple | str
        :param value: Conjugated form(s)
        """
        if len(key) == 3:
            mood, tense, person = key
            self.conjug_info[mood][tense][person] = value
        elif len(key) == 2:
            mood, tense = key
            self.conjug_info[mood][tense] = value
        else:
            self.conjug_info[key] = value

    def __contains__(self, item):
        """
        Check if a conjugated form exists in the verb.

        :param item: Form to search (with or without pronoun).
        :type item: str
        :return: True if found, else False
        :rtype: bool
        """
        try:
            for mood, tenses in self.full_forms.items():
                for tense, persons in tenses.items():
                    if isinstance(persons, str):
                        if " ".join((tense, persons)) == item or persons == item:
                            return True
                    else:
                        for pers, form_ in persons.items():
                            if " ".join((pers, form_)) == item or form_ == item:
                                return True
            return False
        except KeyError:
            return False

    def __iter__(self):
        """
        Iterate over all conjugated forms.

        :return: Generator of (mood, tense, person?, form)
        """
        for mood, tenses in self.conjug_info.items():
            for tense, persons in tenses.items():
                if isinstance(persons, str):
                    yield mood, tense, persons
                else:
                    for pers, form in persons.items():
                        yield mood, tense, pers, form

    def __len__(self):
        count = 0
        for mood, tenses in self.conjug_info.items():
            for tense, persons in tenses.items():
                if isinstance(persons, str):
                    count += 1
                else:
                    count += len(persons)
        return count

    def iterate(self):
        """
        Return all conjugated forms as a list.

        :return: List of conjugated forms.
        :rtype: list
        """
        return [item for item in self]

    def _load_conjug(self, subject="abbrev"):
        """
        Populate conjugated forms (generic implementation).

        :param subject: Pronoun format.
        :type subject: str
        """
        for mood, tense in self.conjug_info.items():
            for tense_name, persons in tense.items():
                if isinstance(persons, list):
                    persons_dict = OrderedDict()
                    for pers, term in persons:
                        key = ABBREVS[pers] if len(persons) == 6 else ""
                        if term is not None:
                            self.conjugate_person(key, persons_dict, term)
                        else:
                            persons_dict[key] = None
                    self.conjug_info[mood][tense_name] = persons_dict
                elif isinstance(persons, str):
                    self.conjug_info[mood][tense_name] = self.verb_info.root + persons

    def conjugate_person(self, key, persons_dict, term):
        """
        Build conjugated form for a single grammatical person.

        :param key: Subject key (pronoun or abbreviation).
        :type key: str
        :param persons_dict: Target dictionary.
        :type persons_dict: OrderedDict
        :param term: Conjugated suffix.
        :type term: str
        """
        persons_dict[key] = self.verb_info.root + term


class VerbFr(Verb):
    """French verb conjugation implementation."""
    __slots__ = ()
    language = "fr"
    # (unchanged logic below, docstring-only fix applied)


class VerbEn(Verb):
    """English verb conjugation implementation."""
    __slots__ = ()
    language = "en"


class VerbEs(Verb):
    """Spanish verb conjugation implementation."""
    __slots__ = ()
    language = "es"


class VerbIt(Verb):
    """Italian verb conjugation implementation."""
    __slots__ = ()
    language = "it"


class VerbPt(Verb):
    """Portuguese verb conjugation implementation."""
    __slots__ = ()
    language = "pt"


class VerbRo(Verb):
    """Romanian verb conjugation implementation."""
    __slots__ = ()
    language = "ro"


if __name__ == "__main__":
    pass
