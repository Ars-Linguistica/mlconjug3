"""
This module defines the VerbInfo and the Verb, VerbFr, VerbEn, VerbEs, VerbIt, VerbPt, VerbRo classes
for representing verb conjugation information.

The VerbInfo class defines the structure for storing information about a verb, including its infinitive form,
lexical root, and ending pattern template.

The Verb class represents a verb with information from a VerbInfo object, a dictionary of conjugation information,
and options for subject pronoun format and whether or not the conjugation information was predicted by a model.
The class also has methods for iterating through the conjugated forms and loading pronoun conjugations.
"""

import abc
from collections import OrderedDict
from mlconjug3.constants import *


class VerbInfo:
    """
    This class defines the Verbiste verb information structure.
    
    :param infinitive: string.
        Infinitive form of the verb.
    :param root: string.
        Lexical root of the verb.
    :param template: string.
        Name of the verb ending pattern.
    :ivar infinitive: string.
        Infinitive form of the verb.
    :ivar root: string.
        Lexical root of the verb.
    :ivar template: string.
        Name of the verb ending pattern.
    """
    __slots__ = ('infinitive', 'root', 'template')

    def __init__(self, infinitive, root, template):
        self.infinitive = infinitive
        if not root:
            self.root = '' if template[0] == ':' else template[:template.index(':')]
        else:
            self.root = root
        self.template = template
        return

    def __repr__(self):
        return '{}.{}({}, {}, {})'.format(__name__, self.__class__.__name__, self.infinitive, self.root, self.template)

    def __eq__(self, other):
        if not isinstance(other, VerbInfo):
            return NotImplemented
        return self.infinitive == other.infinitive and self.root == other.root and self.template == other.template


class VerbMeta(abc.ABCMeta):
    """
    This is a metaclass for creating verb classes.
    It contains the following abstract methods:
    - __init__: Initializes the verb class with verb information, conjugation information, subject (default is 'abbrev') and a flag for whether the verb is predicted or not
    - __getitem__: Allows for indexing of the verb class
    - __setitem__: Allows for setting values of the verb class through indexing
    - __contains__: Allows for checking if a key is present in the verb class
    - __iter__: Allows for iteration over the verb class
    - language: An abstract property that should be implemented to return the language of the verb class
    - iterate: An abstract method that should be implemented to iterate over all forms of the verb
    - load_conjug: An abstract method that should be implemented to load conjugation information for the verb
    - conjugate: An abstract method that should be implemented to conjugate the verb based on the subject and tense provided
    """
    @abc.abstractmethod
    def __init__(self, verb_info, conjug_info, subject='abbrev', predicted=False):
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
    This class defines the Verb Object.
    
    :param verb_info: VerbInfo Object.
    :param conjug_info: OrderedDict.
    :param subject: string.
        Toggles abbreviated or full pronouns.
        The default value is 'abbrev'.
        Select 'pronoun' for full pronouns.
    :param predicted: bool.
        Indicates if the conjugation information was predicted by the model or retrieved from the dataset.
    :ivar verb_info: VerbInfo Object.
    :ivar conjug_info: OrderedDict.
    :ivar confidence_score: float. Confidence score of the prediction accuracy.
    :ivar subject: string. Either 'abbrev' or 'pronoun'
    :ivar predicted: bool.
        Indicates if the conjugation information was predicted by the model or retrieved from the dataset.
    """
    __slots__ = ('name', 'verb_info', 'conjug_info', 'full_forms', 'subject', 'predicted', 'confidence_score')

    language = 'default'

    def __init__(self, verb_info, conjug_info, subject='abbrev', predicted=False):
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
            self._load_conjug("pronoun")
            self.full_forms = self.conjug_info
            self._load_conjug(subject)
        return

    def __repr__(self):
        return '{}.{}({})'.format(__name__, self.__class__.__name__, self.name)

    def __getitem__(self, key):
        """
        Returns the conjugated form of the verb for the specified key.
        
        :param key: tuple of (mood, tense, person) or (mood, tense) or (mood)
        :return: str or dict
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
        Sets the conjugated form of the verb for the specified key.
        
        :param key: tuple of (mood, tense, person) or (mood, tense) or (mood)
        :param value: str or dict
        :return: None
        """
        if len(key) == 3:
            mood, tense, person = key
            self.conjug_info[mood][tense][person] = value
        elif len(key) == 2:
            mood, tense = key
            self.conjug_info[mood][tense] = value
        else:
            self.conjug_info[key] = value
        return
    
    def __contains__(self, item):
        """
        The method checks if the provided form exists in the conjugated forms of the verb.
        It can accept statements such as '"tu manges " in verb', '"manges" in verb' etc...
        It will iterate over the conjugated forms and check if the form is present in the
        full_forms attribute of the object.
        
        :param item: string in the format 'pronoun form' like 'tu manges' or just the verbal form like 'mangeras'.
        :return: bool
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
        Lazy generator that returns all conjugated forms of the verb as tuples of (mood, tense, person, form)
        """
        for mood, tenses in self.conjug_info.items():
            for tense, persons in tenses.items():
                if isinstance(persons, str):
                    yield mood, tense, persons
                else:
                    for pers, form in persons.items():
                        yield mood, tense, pers, form
    
    def __len__(self):
        """
        Returns the number of conjugated forms of the verb
        """
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
        Iterates over all conjugated forms and returns a list of tuples of those conjugated forms.
        
        :return conjugated_forms: generator.
            Lazy generator of conjugated forms.
        """
        return [item for item in self]

    def _load_conjug(self, subject="abbrev"):
        """
        | Populates the inflected forms of the verb.
        | This is the generic version of this method.
        | It does not add personal pronouns to the conjugated forms.
        | This method can handle any new language if the conjugation structure conforms to the Verbiste XML Schema.
        """
        for mood, tense in self.conjug_info.items():
            for tense_name, persons in tense.items():
                if isinstance(persons, list):
                    persons_dict = OrderedDict()
                    for pers, term in persons:
                        key = ABBREVS[pers] if len(persons) == 6 else ''
                        if term is not None:
                            self.conjugate_person(key, persons_dict, term)
                        else:
                            persons_dict[key] = None
                    self.conjug_info[mood][tense_name] = persons_dict
                elif isinstance(persons, str):
                    self.conjug_info[mood][tense_name] = self.verb_info.root + persons
        return

    def conjugate_person(self, key, persons_dict, term):
        """
        Creates the conjugated form of the person specified by the key argument.
        
        :param key: string.
        :param persons_dict: OrderedDict
        :param term: string.
        :return: None.
        """
        persons_dict[key] = self.verb_info.root + term
        return


class VerbFr(Verb):
    """
    This class defines the French Verb Object.
    """
    __slots__ = ()

    language = 'fr'

    def _load_conjug(self, subject):
        """
        | Populates the inflected forms of the verb.
        | Adds personal pronouns to the inflected verbs.
        """
        for mood, tense in self.conjug_info.items():
            for tense_name, persons in tense.items():
                if isinstance(persons, list):
                    persons_dict = OrderedDict()
                    for pers, term in persons:
                        if len(persons) == 6:
                            key = PRONOUNS[self.language][subject][pers]
                        elif tense_name == 'Participe Passé':
                            key = GENDER[self.language][subject][pers]
                        elif tense_name == 'Imperatif Présent':
                            key = IMPERATIVE_PRONOUNS[self.language][subject][pers]
                        else:
                            key = term
                        if term is not None:
                            self.conjugate_person(key, persons_dict, term)
                        else:
                            persons_dict[key] = None
                    self.conjug_info[mood][tense_name] = persons_dict
                elif isinstance(persons, str):
                    self.conjug_info[mood][tense_name] = self.verb_info.root + persons
        return


class VerbEn(Verb):
    """
    This class defines the English Verb Object.
    """
    __slots__ = ()

    language = 'en'

    def _load_conjug(self, subject):
        """
        | Populates the inflected forms of the verb.
        | Adds personal pronouns to the inflected verbs.
        """
        for mood, tense in self.conjug_info.items():
            for tense_name, persons in tense.items():
                if isinstance(persons, list):
                    persons_dict = OrderedDict()
                    for pers, term in persons:
                        if len(persons) == 6:
                            key = PRONOUNS[self.language][subject][pers]
                        elif tense_name == 'imperative present':
                            key = IMPERATIVE_PRONOUNS[self.language][subject][pers]
                        else:
                            key = 'to'
                        if term is not None:
                            self.conjugate_person(key, persons_dict, term)
                        else:
                            self.conjugate_person(key, persons_dict, '')
                    self.conjug_info[mood][tense_name] = persons_dict
                elif isinstance(persons, str):
                    prefix = 'to ' if tense_name == 'infinitive present' else ''
                    if tense_name == 'infinitive present':
                        self.conjug_info[mood][tense_name] = prefix + self.verb_info.infinitive
                    else:
                        self.conjug_info[mood][tense_name] = prefix + self.verb_info.root + persons
                elif persons is None:
                    prefix = 'to ' if tense_name == 'infinitive present' else ''
                    self.conjug_info[mood][tense_name] = prefix + self.verb_info.infinitive
        return


class VerbEs(Verb):
    """
    This class defines the Spanish Verb Object.
    """
    __slots__ = ()

    language = 'es'

    def _load_conjug(self, subject):
        """
        | Populates the inflected forms of the verb.
        | Adds personal pronouns to the inflected verbs.
        """
        for mood, tense in self.conjug_info.items():
            for tense_name, persons in tense.items():
                if isinstance(persons, list):
                    persons_dict = OrderedDict()

                    for pers, term in persons:
                        if len(persons) == 5 and not tense_name.startswith('Imperativo'):
                            continue
                        if len(persons) == 6:
                            key = PRONOUNS[self.language][subject][pers]
                        elif tense_name == 'Imperativo Afirmativo':
                            key = IMPERATIVE_PRONOUNS[self.language][subject][pers]
                        elif tense_name == 'Imperativo non':
                            key = ' '.join((IMPERATIVE_PRONOUNS[self.language][subject][pers],
                                            NEGATION[self.language]))
                        elif tense_name == 'Gerundio Gerondio':
                            if term.endswith('ndo'):
                                key = ''
                            else:
                                continue
                        elif tense_name == 'Infinitivo Infinitivo':
                            if term.endswith('r'):
                                key = ''
                            else:
                                continue
                        else:
                            key = pers
                        if term is not None and term != '-':
                            self.conjugate_person(key, persons_dict, term)
                        else:
                            persons_dict[key] = None
                    self.conjug_info[mood][tense_name] = persons_dict
                elif isinstance(persons, str):
                    self.conjug_info[mood][tense_name] = self.verb_info.root + persons
        return


class VerbIt(Verb):
    """
    This class defines the Italian Verb Object.
    """
    __slots__ = ()

    language = 'it'

    def _load_conjug(self, subject):
        """
        | Populates the inflected forms of the verb.
        | Adds personal pronouns to the inflected verbs.
        """
        for mood, tense in self.conjug_info.items():
            for tense_name, persons in tense.items():
                if isinstance(persons, list):
                    persons_dict = OrderedDict()
                    for pers, term in persons:
                        if len(persons) == 6 and not tense_name.startswith('Imperativo'):
                            key = PRONOUNS[self.language][subject][pers]
                        elif tense_name.startswith('Imperativo'):
                            key = PRONOUNS[self.language]['abbrev'][pers]
                        else:
                            key = pers
                        if term is not None and term != '-':
                            if tense_name == 'Imperativo non':
                                persons_dict[key] = ' '.join((NEGATION[self.language], self.verb_info.root + term))
                            else:
                                self.conjugate_person(key, persons_dict, term)
                        else:
                            persons_dict[key] = None
                    self.conjug_info[mood][tense_name] = persons_dict
                elif isinstance(persons, str):
                    self.conjug_info[mood][tense_name] = self.verb_info.root + persons
        return


class VerbPt(Verb):
    """
    This class defines the Portuguese Verb Object.
    """
    __slots__ = ()

    language = 'pt'

    def _load_conjug(self, subject):
        """
        | Populates the inflected forms of the verb.
        | Adds personal pronouns to the inflected verbs.
        """
        for mood, tense in self.conjug_info.items():
            for tense_name, persons in tense.items():
                if isinstance(persons, list):
                    persons_dict = OrderedDict()
                    for pers, term in persons:
                        if len(persons) == 6 and not tense_name.startswith('Imperativo'):
                            key = PRONOUNS[self.language][subject][pers]
                        elif tense_name.startswith('Imperativo'):
                            key = PRONOUNS[self.language]['abbrev'][pers]
                        else:
                            key = pers
                        if term is not None and term != '-':
                            if tense_name == 'Imperativo Negativo':
                                persons_dict[key] = ' '.join((NEGATION[self.language], self.verb_info.root + term))
                            else:
                                self.conjugate_person(key, persons_dict, term)
                        else:
                            persons_dict[key] = None
                    self.conjug_info[mood][tense_name] = persons_dict
                elif isinstance(persons, str):
                    self.conjug_info[mood][tense_name] = self.verb_info.root + persons
        return


class VerbRo(Verb):
    """
    This class defines the Romanian Verb Object.
    """
    __slots__ = ()

    language = 'ro'

    def _load_conjug(self, subject):
        """
        | Populates the inflected forms of the verb.
        | Adds personal pronouns to the inflected verbs.
        """
        for mood, tense in self.conjug_info.items():
            for tense_name, persons in tense.items():
                if isinstance(persons, list):
                    persons_dict = OrderedDict()
                    for pers, term in persons:
                        if len(persons) == 6:
                            key = PRONOUNS[self.language][subject][pers]
                        elif tense_name.startswith('Imperativ Imperativ'):
                            key = IMPERATIVE_PRONOUNS[self.language][subject][pers]
                        elif tense_name == 'Imperativ Negativ':
                            key = NEGATION[self.language]
                        else:
                            key = pers
                        if term is not None and term != '-':
                            if tense_name == 'Imperativ Negativ':
                                persons_dict[key] = ' '.join((NEGATION[self.language], self.verb_info.root + term))
                            else:
                                self.conjugate_person(key, persons_dict, term)
                        else:
                            persons_dict[key] = None
                    self.conjug_info[mood][tense_name] = persons_dict
                elif isinstance(persons, str):
                    prefix = 'a ' if tense_name == 'Infinitiv Afirmativ' else ''
                    self.conjug_info[mood][tense_name] = prefix + self.verb_info.root + persons
        return

if __name__ == "__main__":
    pass
