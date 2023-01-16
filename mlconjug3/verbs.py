import json
from collections import OrderedDict

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
    
    def __len__(self):
        return sum(len(tenses) for tenses in self.conjug_info.values())

    
    def __getitem__(self, key):
        try:
            return self.conjug_info[key]
        except KeyError:
            raise KeyError(f"{key} not found in conjugation information")
            
    def __iter__(self):
        """
        Iterates over all conjugated forms and returns a lazy generator of tuples of those conjugated forms.
        :return: generator.
            Lazy generator of conjugated forms.
        """
        for mood, tenses in self.conjug_info.items():
            for tense, persons in tenses.items():
                if isinstance(persons, str):
                    yield (mood, tense, persons)
                else:
                    for pers, form in persons.items():
                        yield (mood, tense, pers, form)

    
    def __eq__(self, other):
        if not isinstance(other, Verb):
            return NotImplemented
        return (self.name == other.name and 
                self.verb_info == other.verb_info and 
                self.conjug_info == other.conjug_info and 
                self.subject == other.subject and
                self.predicted == other.predicted)
    
    def __call__(self, mood, tense, person):
        try:
            return self.conjug_info[mood][tense][person]
        except KeyError:
            raise KeyError(f"{mood} {tense} {person} not found in conjugation information")



    def iterate(self):
        """
        Iterates over all conjugated forms and returns a lazy generator of tuples of those conjugated forms.
        :return: generator.
            Lazy generator of conjugated forms.
        """
        for mood, tenses in self.conjug_info.items():
            for tense, persons in tenses.items():
                if isinstance(persons, str):
                    yield (mood, tense, persons)
                else:
                    for pers, form in persons.items():
                        yield (mood, tense, pers, form)


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
    

class VerbFactory:
    def create_verb(language, infinitive, root, template):
        if language not in _VERBS:
            raise ValueError(f"Invalid language: {language}")
        return _VERBS[language](infinitive, root, template)

    
class ConjugationDecorator:
    def __init__(self, verb):
        self._verb = verb

    def add_conjugation(self, mood, tense, person, form):
        self._verb.conjug_info[mood][tense][person] = form

        
class LanguageDetector:
    def __init__(self, model_path):
        self.model = joblib.load(model_path)
        
    def detect(self, infinitive: str):
        features = VerbFeatures.extract_verb_features(infinitive)
        return self.model.predict([features])

    
