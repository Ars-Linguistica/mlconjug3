"""
PyVerbiste.

| A Python library for conjugating verbs in French, English, Spanish, Italian, Portuguese and Romanian (more soon).
| It contains conjugation data generated by machine learning models using the python library mlconjug3.
| More information about mlconjug3 at https://pypi.org/project/mlconjug3/


| The conjugation data conforms to the XML schema defined by Verbiste.
| More information on Verbiste at https://perso.b2b2c.ca/~sarrazip/dev/conjug_manager.html

"""

__author__ = 'SekouDiaoNlp'
__author_email__ = 'diao.sekou.nlp@gmail.com'


import copy
import defusedxml.ElementTree as ET
import json
from collections import OrderedDict
import pkg_resources


_RESOURCE_PACKAGE = 'mlconjug3'

_LANGUAGES = ('default', 'fr', 'en', 'es', 'it', 'pt', 'ro')

_VERBS_RESOURCE_PATH = {'fr': '/'.join(('data', 'conjug_manager', 'verbs-fr.json')),
                        'it': '/'.join(('data', 'conjug_manager', 'verbs-it.json')),
                        'es': '/'.join(('data', 'conjug_manager', 'verbs-es.json')),
                        'en': '/'.join(('data', 'conjug_manager', 'verbs-en.json')),
                        'pt': '/'.join(('data', 'conjug_manager', 'verbs-pt.json')),
                        'ro': '/'.join(('data', 'conjug_manager', 'verbs-ro.json')),}

_CONJUGATIONS_RESOURCE_PATH = {'fr': '/'.join(('data', 'conjug_manager', 'conjugation-fr.json')),
                               'it': '/'.join(('data', 'conjug_manager', 'conjugation-it.json')),
                               'es': '/'.join(('data', 'conjug_manager', 'conjugation-es.json')),
                               'en': '/'.join(('data', 'conjug_manager', 'conjugation-en.json')),
                               'pt': '/'.join(('data', 'conjug_manager', 'conjugation-pt.json')),
                               'ro': '/'.join(('data', 'conjug_manager', 'conjugation-ro.json')),}

_ABBREVS = ("1s", "2s", "3s", "1p", "2p", "3p")

_PRONOUNS = {'fr': {'abbrev': _ABBREVS,
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

_IMPERATIVE_PRONOUNS = {'fr': {'abbrev': ("2s", "1p", "2p"),
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

_AUXILIARIES = {'fr': None,
                'it': 'non',
                'es': 'no',
                'en': None,
                'pt': 'não',
                'ro': 'nu'}

_GENDER = {'fr': {'abbrev': ("ms", "mp", "fs", "fp"),
                  'pronoun': ("masculin singulier", "masculin pluriel", "feminin singulier", "feminin pluriel")},
           'it': None,
           'es': None,
           'en': None,
           'pt': None,
           'ro': None}

_NEGATION = {'fr': 'ne',
             'it': 'non',
             'es': 'no',
             'en': "don't",
             'pt': 'não',
             'ro': 'nu'}


class ConjugManager:
    """
        This is the class handling the mlconjug3 json files.

        :param language: string.
            | The language of the conjugator. The default value is fr for French.
            | The allowed values are: fr, en, es, it, pt, ro.
        :ivar language: Language of the conjugator.
        :ivar verbs: Dictionary where the keys are verbs and the values are conjugation patterns.
        :ivar conjugations: Dictionary where the keys are conjugation patterns and the values are inflected forms.

        """

    def __init__(self, language='default'):
        if language not in _LANGUAGES:
            raise ValueError(_('Unsupported language.\nThe allowed languages are fr, en, es, it, pt, ro.'))
        self.language = 'fr' if language == 'default' else language
        self.verbs = {}
        self.conjugations = OrderedDict()
        verbs_file = pkg_resources.resource_filename(_RESOURCE_PACKAGE, _VERBS_RESOURCE_PATH[self.language])
        self._load_verbs(verbs_file)
        self._allowed_endings = self._detect_allowed_endings()
        conjugations_file = pkg_resources.resource_filename(_RESOURCE_PACKAGE,
                                                            _CONJUGATIONS_RESOURCE_PATH[self.language])
        self._load_conjugations(conjugations_file)
        self.templates = sorted(self.conjugations.keys())
        return

    def __repr__(self):
        return '{}.{}(language={})'.format(__name__, self.__class__.__name__, self.language)

    def _load_verbs(self, verbs_file):
        """
        Load and parses the verbs from the json file.

        :param verbs_file: string or path object.
            Path to the verbs json file.

        """
        with open(verbs_file, encoding='utf-8') as file:
            self.verbs = json.load(file)
        return

    def _load_conjugations(self, conjugations_file):
        """
        Load and parses the conjugations from the json file.

        :param conjugations_file: string or path object.
            Path to the conjugation json file.

        """
        with open(conjugations_file, encoding='utf-8') as file:
            self.conjugations = json.load(file)
        return

    def _detect_allowed_endings(self):
        """
        | Detects the allowed endings for verbs in the supported languages.
        | All the supported languages except for English restrict the form a verb can take.
        | As English is much more productive and varied in the morphology of its verbs, any word is allowed as a verb.

        :return: set.
            A set containing the allowed endings of verbs in the target language.

        """
        if self.language == 'en':
            return set()
        return {verb.split(' ')[0][-2:] for verb in self.verbs if len(verb) >= 2}

    def is_valid_verb(self, verb):
        """
        | Checks if the verb is a valid verb in the given language.
        | English words are always treated as possible verbs.
        | Verbs in other languages are filtered by their endings.

        :param verb: string.
            The verb to conjugate.
        :return: bool.
            True if the verb is a valid verb in the language. False otherwise.

        """
        if self.language == 'en':
            return True  # LOL!
        return verb[-2:] in self._allowed_endings

    def get_verb_info(self, verb):
        """
        Gets verb information and returns a VerbInfo instance.

        :param verb: string.
            Verb to conjugate.
        :return: VerbInfo object or None.

        """
        if verb not in self.verbs.keys():
            return None
        infinitive = verb
        root = self.verbs[verb]['root']
        template = self.verbs[verb]['template']
        return VerbInfo(infinitive, root, template)

    def get_conjug_info(self, template):
        """
        Gets conjugation information corresponding to the given template.

        :param template: string.
            Name of the verb ending pattern.
        :return: OrderedDict or None.
            OrderedDict containing the conjugated suffixes of the template.

        """
        if template not in self.conjugations.keys():
            return None
        return copy.deepcopy(self.conjugations[template])


class Verbiste(ConjugManager):
    """
    This is the class handling the Verbiste xml files.

    :param language: string.
        | The language of the conjugator. The default value is fr for French.
        | The allowed values are: fr, en, es, it, pt, ro.
    :ivar language: Language of the conjugator.
    :ivar verbs: Dictionary where the keys are verbs and the values are conjugation patterns.
    :ivar conjugations: Dictionary where the keys are conjugation patterns and the values are inflected forms.

    """

    def _load_verbs(self, verbs_file):
        """
        Load and parses the verbs from the xml file.

        :param verbs_file: string or path object.
            Path to the verbs xml file.

        """
        self.verbs = self._parse_verbs(verbs_file.replace('json', 'xml'))
        return

    @staticmethod
    def _parse_verbs(file):
        """
        Parses the XML file.

        :param file: FileObject.
            XML file containing the verbs.
        :return: OrderedDict.
            An OrderedDict containing the verb and its template for all verbs in the file.

        """
        verbs_dic = {}
        xml = ET.parse(file)
        for verb in xml.findall("v"):
            verb_name = verb.find("i").text
            template = verb.find("t").text
            index = - len(template[template.index(":") + 1:])
            root = verb_name if index == 0 else verb_name[:index]
            verbs_dic[verb_name] = {"template": template, "root": root}
        return verbs_dic

    def _load_conjugations(self, conjugations_file):
        """
        Load and parses the conjugations from the xml file.

        :param conjugations_file: string or path object.
            Path to the conjugation xml file.

        """
        self.conjugations = self._parse_conjugations(conjugations_file.replace('json', 'xml'))
        return

    def _parse_conjugations(self, file):
        """
        Parses the XML file.

        :param file: FileObject.
            XML file containing the conjugation templates.
        :return: OrderedDict.
            An OrderedDict containing all the conjugation templates in the file.

        """
        conjugations_dic = {}
        xml = ET.parse(file)
        for template in xml.findall("template"):
            template_name = template.get("name")
            conjugations_dic[template_name] = OrderedDict()
            for mood in list(template):
                conjugations_dic[template_name][mood.tag] = OrderedDict()
                for tense in list(mood):
                    conjugations_dic[template_name][mood.tag][tense.tag.replace('-', ' ')] = self._load_tense(tense)
        return conjugations_dic

    @staticmethod
    def _load_tense(tense):
        """
        Load and parses the inflected forms of the tense from xml file.

        :param tense: list of xml tags containing inflected forms.
            The list of inflected forms for the current tense being processed.
        :return: list.
            List of inflected forms.

        """
        persons = list(tense)
        if not persons:
            return None
        elif len(persons) == 1:
            if persons[0].find("i") is None:
                return None
            conjug = persons[0].find("i").text
        else:
            conjug = []
            for pers, term in enumerate(persons):
                if term.find("i") is not None:
                    if term.find("i").text is not None:
                        conjug.append((pers, term.find("i").text))
                    else:
                        conjug.append((pers, ''))
                else:
                    conjug.append((pers, None))
        return conjug


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
        return '{}.{}({})'.format(__name__, self.__class__.__name__, self.name)

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
                        key = _ABBREVS[pers] if len(persons) == 6 else ''
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


if __name__ == "__main__":
    pass
