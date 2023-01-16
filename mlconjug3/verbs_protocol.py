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


    def __str__(self):
        return 'Infinitive: {0}, Root: {1}, Template: {2}'.format(self.infinitive, self.root, self.template)

    def __len__(self):
        """
        The __len__ method allows the use of the built-in len() function on an instance of the class.
        It returns the number of attributes in the class
        """
        return len(self.__slots__)

    def __eq__(self, other):
        if not isinstance(other, VerbInfo):
            return NotImplemented
        return self.infinitive == other.infinitive and self.root == other.root and self.template == other.template

    def __getitem__(self, key):
        if key not in self.__slots__:
            raise KeyError("Invalid key")
        return getattr(self, key)


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
