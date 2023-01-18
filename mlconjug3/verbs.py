import json
from collections import OrderedDict
from .constants import *
from .utils import logger

# from immutabledict import immutabledict, ImmutableOrderedDict

RESOURCE_PACKAGE = 'mlconjug3'

LANGUAGES = ('default', 'fr', 'en', 'es', 'it', 'pt', 'ro')

VERBS_RESOURCE_PATH = {'fr': '/'.join(('data', 'conjug_manager', 'verbs-fr.json')),
                        'it': '/'.join(('data', 'conjug_manager', 'verbs-it.json')),
                        'es': '/'.join(('data', 'conjug_manager', 'verbs-es.json')),
                        'en': '/'.join(('data', 'conjug_manager', 'verbs-en.json')),
                        'pt': '/'.join(('data', 'conjug_manager', 'verbs-pt.json')),
                        'ro': '/'.join(('data', 'conjug_manager', 'verbs-ro.json')),}

CONJUGATIONS_RESOURCE_PATH = {'fr': '/'.join(('data', 'conjug_manager', 'conjugation-fr.json')),
                               'it': '/'.join(('data', 'conjug_manager', 'conjugation-it.json')),
                               'es': '/'.join(('data', 'conjug_manager', 'conjugation-es.json')),
                               'en': '/'.join(('data', 'conjug_manager', 'conjugation-en.json')),
                               'pt': '/'.join(('data', 'conjug_manager', 'conjugation-pt.json')),
                               'ro': '/'.join(('data', 'conjug_manager', 'conjugation-ro.json')),}

ABBREVS = ("1s", "2s", "3s", "1p", "2p", "3p")

PRONOUNS = {'fr': {'abbrev': _ABBREVS,
                    'pronoun': ("je", "tu", "il (elle, on)", "nous", "vous", "ils (elles)")},
             'it': {'abbrev': _ABBREVS,
                    'pronoun': ('io', 'tu', 'egli/ella', 'noi', 'voi', 'essi/esse')},
             'es': {'abbrev': _ABBREVS,
                    'pronoun': ('yo', 'tú', 'él', 'nosotros', 'vosotros', 'ellos')},
             'en': {'abbrev': _ABBREVS,
                    'pronoun': ('I', 'you', 'he/she/it', 'you', 'we', 'they')},
             'pt': {'abbrev': _ABBREVS,
                    'pronoun': ('eu', 'tu', 'ele', 'nós', 'vós', 'eles')},
             'ro': {'abbrev': _ABBREVS,
                    'pronoun': ('eu', 'tu', 'el/ea', 'noi', 'voi', 'ei/ele')}
             }

IMPERATIVE_PRONOUNS = {'fr': {'abbrev': ("2s", "1p", "2p"),
                               'pronoun': ("", "", "")},
                        'it': None,
                        'es': {'abbrev': ("2s", "3s", "1p", "2p", "3p"),
                               'pronoun': ('tú', 'él', 'nosotros', 'vosotros', 'ellos')},
                        'en': {'abbrev': ("2s", "1p", "2p"),
                               'pronoun': ("", "let's", "")},
                        'pt': None,
                        'ro': {'abbrev': ("2s", "2p"),
                               'pronoun': ("tu", "voi")},
                        }

AUXILIARIES = {'fr': None,
                'it': 'non',
                'es': 'no',
                'en': None,
                'pt': 'não',
                'ro': 'nu'}

GENDER = {'fr': {'abbrev': ("ms", "mp", "fs", "fp"),
                  'pronoun': ("masculin singulier", "masculin pluriel", "feminin singulier", "feminin pluriel")},
           'it': None,
           'es': None,
           'en': None,
           'pt': None,
           'ro': None}

NEGATION = {'fr': 'ne',
             'it': 'non',
             'es': 'no',
             'en': "don't",
             'pt': 'não',
             'ro': 'nu'}


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

    language = 'default'

    def __init__(self, verb_info, conjug_info, subject='abbrev', predicted=False):
        self.name = verb_info.infinitive
        self.verb_info = verb_info
        self.conjug_info = conjug_info
        self.subject = subject
        self.predicted = predicted
        self.confidence_score = None
        self._load_conjug()
        return

    def __repr__(self):
        return '{0}.{1}({2})'.format(__name__, self.__class__.__name__, self.name)

    def iterate(self):
        """
        Iterates over all conjugated forms and returns a list of tuples of those conjugated forms.
        :return: list.
            List of conjugated forms.
        """
        iterate_results = []
        for mood, tenses in self.conjug_info.items():
            for tense, persons in tenses.items():
                if isinstance(persons, str):
                    iterate_results.append((mood, tense, persons))
                else:
                    for pers, form in persons.items():
                        iterate_results.append((mood, tense, pers, form))
        return iterate_results

    def _load_conjug(self):
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
                            key = PRONOUNS[self.language][self.subject][pers]
                        elif tense_name == 'Participe Passé':
                            key = GENDER[self.language][self.subject][pers]
                        elif tense_name == 'Imperatif Présent':
                            key = IMPERATIVE_PRONOUNS[self.language][self.subject][pers]
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
                            key = PRONOUNS[self.language][self.subject][pers]
                        elif tense_name == 'imperative present':
                            key = IMPERATIVE_PRONOUNS[self.language][self.subject][pers]
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
                            key = PRONOUNS[self.language][self.subject][pers]
                        elif tense_name == 'Imperativo Afirmativo':
                            key = IMPERATIVE_PRONOUNS[self.language][self.subject][pers]
                        elif tense_name == 'Imperativo non':
                            key = ' '.join((IMPERATIVE_PRONOUNS[self.language][self.subject][pers],
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
                            key = PRONOUNS[self.language][self.subject][pers]
                        elif tense_name.startswith('Imperativo'):
                            key = PRONOUNS[self.language]['abbrev'][pers]
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
                            key = PRONOUNS[self.language][self.subject][pers]
                        elif tense_name.startswith('Imperativo'):
                            key = PRONOUNS[self.language]['abbrev'][pers]
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
                            key = PRONOUNS[self.language][self.subject][pers]
                        elif tense_name.startswith('Imperativ Imperativ'):
                            key = IMPERATIVE_PRONOUNS[self.language][self.subject][pers]
                        elif tense_name == 'Imperativ Negativ':
                            key = NEGATION[self.language]
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
