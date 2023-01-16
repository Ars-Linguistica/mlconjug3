import json
from collections import OrderedDict
import concurrent.futures
from functools import lru_cache

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
        return '{0}.{1}({2}, {3}, {4})'.format(__name__, self.__class__.__name__, self.infinitive, self.root, self.template)

    def __eq__(self, other):
        if not isinstance(other, VerbInfo):
            return NotImplemented
        return self.infinitive == other.infinitive and self.root == other.root and self.template == other.template

    
class ParallelVerb(Verb):
    def _load_conjugation(self):
        if self.verb_info.infinitive not in self._conjug_cache:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(self._load_conjugation_thread, self.verb_info.infinitive)
                self._conjug_cache[self.verb_info.infinitive] = future.result()
            return self._conjug_cache[self.verb_info.infinitive]
    
    def _load_conjugation_thread(self, verb_infinitive):
        with open("conjugation_data/{}_conjugations.json".format(verb_infinitive), "r") as conjug_file:
            conjug_info = json.load(conjug_file)
        return conjug_info

    
class Verb:
    """
    This class defines the Verb Object.
    :param verb_info: VerbInfo Object.
    :param subject: string.
        Toggles abbreviated or full pronouns.
        The default value is 'abbrev'.
        Select 'pronoun' for full pronouns.
    :param predicted: bool.
        Indicates if the conjugation information was predicted by the model or retrieved from the dataset.
    :ivar verb_info: VerbInfo Object.
    :ivar subject: string. Either 'abbrev' or 'pronoun'
    :ivar predicted: bool.
        Indicates if the conjugation information was predicted by the model or retrieved from the dataset.
    """
    __slots__ = ('name', 'verb_info', 'subject', 'predicted', 'confidence_score')
    _conjug_cache = {}

    def __init__(self, verb_info, subject='abbrev', predicted=False):
        self.name = verb_info.infinitive
        self.verb_info = verb_info
        self.subject = subject
        self.predicted = predicted

    def _load_conjugation(self):
        if self.verb_info.infinitive not in self._conjug_cache:
            # load conjugation information for verb
            with open("conjugation_data/{}_conjugations.json".format(self.verb_info.infinitive), "r") as conjug_file:
                conjug_info = json.load(conjug_file)
                self._conjug_cache[self.verb_info.infinitive] = conjug_info
        return self._conjug_cache[self.verb_info.infinitive]
    
    @lru_cache(maxsize=None)
    def iterate(self, mood=None, tense=None, person=None):
        """
        Returns a generator of conjugated forms of the verb.
        :param mood: string. Mood to filter by.
        :param tense: string. Tense to filter by.
        :param person: string. Person to filter by.
        :return: generator of conjugated forms of the verb.
        """
        conjug_info = self._load_conjugation()
        for mood_name, mood_conjug in conjug_info.items():
            if mood and mood_name != mood:
                continue
            for tense_name, tense_conjug in mood_conjug.items():
                if tense and tense_name != tense:
                    continue
                for person_name, conjug in tense_conjug.items():
                    if person and person_name != person:
                        continue
                    yield conjug

    def conjugate(self, mood, tense, person):
        """
        Returns the conjugated form of the verb for the specified mood, tense, and person.
        :param mood: string. Mood to filter by.
        :param tense: string. Tense to filter by.
        :param person: string. Person to filter by.
        :return: conjugated form of the verb.
        """
        conjug_info = self._load_conjugation()
        return conjug_info[mood][tense][person]
    
    
class Verb:
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
    __slots__ = ('name', 'verb_info', 'conjug_info', 'subject', 'predicted', 'confidence_score')


class VerbFr(Verb):
    """
    This class defines the French Verb Object.

    """
    __slots__ = ()

    language = 'fr'

    def _load_conjug(self):
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
                            key = _PRONOUNS[self.language][self.subject][pers]
                        elif tense_name == 'Participe Passé':
                            key = _GENDER[self.language][self.subject][pers]
                        elif tense_name == 'Imperatif Présent':
                            key = _IMPERATIVE_PRONOUNS[self.language][self.subject][pers]
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

    def _load_conjug(self):
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
                            key = _PRONOUNS[self.language][self.subject][pers]
                        elif tense_name == 'imperative present':
                            key = _IMPERATIVE_PRONOUNS[self.language][self.subject][pers]
                        else:
                            key = 'to'
                        if term is not None:
                            self.conjugate_person(key, persons_dict, term)
                        else:
                            self.conjugate_person(key, persons_dict, '')
                    self.conjug_info[mood][tense_name] = persons_dict
                elif isinstance(persons, str):
                    prefix = 'to ' if tense_name == 'infinitive present' else ''
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

    def _load_conjug(self):
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
                            key = _PRONOUNS[self.language][self.subject][pers]
                        elif tense_name == 'Imperativo Afirmativo':
                            key = _IMPERATIVE_PRONOUNS[self.language][self.subject][pers]
                        elif tense_name == 'Imperativo non':
                            key = ' '.join((_IMPERATIVE_PRONOUNS[self.language][self.subject][pers],
                                            _NEGATION[self.language]))
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

    def _load_conjug(self):
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
                            key = _PRONOUNS[self.language][self.subject][pers]
                        elif tense_name.startswith('Imperativo'):
                            key = _PRONOUNS[self.language]['abbrev'][pers]
                        else:
                            key = pers
                        if term is not None and term != '-':
                            if tense_name == 'Imperativo non':
                                persons_dict[key] = ' '.join((_NEGATION[self.language], self.verb_info.root + term))
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

    def _load_conjug(self):
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
                            key = _PRONOUNS[self.language][self.subject][pers]
                        elif tense_name.startswith('Imperativo'):
                            key = _PRONOUNS[self.language]['abbrev'][pers]
                        else:
                            key = pers
                        if term is not None and term != '-':
                            if tense_name == 'Imperativo Negativo':
                                persons_dict[key] = ' '.join((_NEGATION[self.language], self.verb_info.root + term))
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

    def _load_conjug(self):
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
                            key = _PRONOUNS[self.language][self.subject][pers]
                        elif tense_name.startswith('Imperativ Imperativ'):
                            key = _IMPERATIVE_PRONOUNS[self.language][self.subject][pers]
                        elif tense_name == 'Imperativ Negativ':
                            key = _NEGATION[self.language]
                        else:
                            key = pers
                        if term is not None and term != '-':
                            if tense_name == 'Imperativ Negativ':
                                persons_dict[key] = ' '.join((_NEGATION[self.language], self.verb_info.root + term))
                            else:
                                self.conjugate_person(key, persons_dict, term)
                        else:
                            persons_dict[key] = None
                    self.conjug_info[mood][tense_name] = persons_dict
                elif isinstance(persons, str):
                    prefix = 'a ' if tense_name == 'Infinitiv Afirmativ' else ''
                    self.conjug_info[mood][tense_name] = prefix + self.verb_info.root + persons
        return
