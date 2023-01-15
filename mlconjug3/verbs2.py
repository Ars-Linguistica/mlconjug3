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

    def __len__(self):
        return len(self.conjug_info)

    def __format__(self, format_spec):
        return "Infinitive form: {}\nConjugated forms: {}".format(self.name, json.dumps(self.conjug_info, indent=4))

    def __getattr__(self, name):
        if name in self.conjug_info:
            return self.conjug_info[name]
        else:
            raise AttributeError("'{}' object has no attribute '{}'".format(self.__class__.__name__, name))

    def __getitem__(self, key):
        if key in self.conjug_info:
            return self.conjug_info[key]
        else:
            raise KeyError("'{}' object has no key '{}'".format(self.__class__.__name__, key))

    def __iter__(self):
        return iter(self.conjug_info)

    def __contains__(self, item):
        return item in self.conjug_info

    def __add__(self, other):
        if not isinstance(other, Verb):
            return NotImplemented
        return self.conjug_info + other.conjug_info

    def __eq__(self, other):
        if not isinstance(other, Verb):
            return NotImplemented
        return self.verb_info == other.verb_info

    def __str__(self):
        return self.name

    def __bool__(self):
        return bool(self.conjug_info)

    def __call__(self, mood, tense, person):
        if mood not in self.conjug_info:
raise ValueError(f"Invalid mood '{mood}' for verb '{self.name}'")
if tense not in self.conjug_info[mood]:
raise ValueError(f"Invalid tense '{tense}' for verb '{self.name}' and mood '{mood}'")
if person not in self.conjug_info[mood][tense]:
raise ValueError(f"Invalid person '{person}' for verb '{self.name}', mood '{mood}' and tense '{tense}'")
return self.conjug_info[mood][tense][person]

    def __len__(self):
    return sum(len(tenses) for mood, tenses in self.conjug_info.items())

def __format__(self, format_spec):
    return json.dumps(self.conjug_info, indent=4)

def __getattr__(self, name):
    for mood, tenses in self.conjug_info.items():
        for tense, persons in tenses.items():
            if name in persons:
                return persons[name]
    raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

def __getitem__(self, key):
    for mood, tenses in self.conjug_info.items():
        for tense, persons in tenses.items():
            if key in persons:
                return persons[key]
    raise KeyError(f"Invalid key '{key}'")

def __iter__(self):
    for mood, tenses in self.conjug_info.items():
        for tense, persons in tenses.items():
            for person, conjug in persons.items():
                yield (mood, tense, person, conjug)

def __contains__(self, item):
    for mood, tenses in self.conjug_info.items():
        for tense, persons in tenses.items():
            if item in persons.values():
                return True
    return False

def __add__(self, other):
    if not isinstance(other, Verb):
        raise TypeError("Cannot concatenate 'Verb' and '{}' objects".format(type(other)))
    return OrderedDict(self.conjug_info, **other.conjug_info)

def __eq__(self, other):
    if not isinstance(other, Verb):
        return NotImplemented
    return self.name == other.name

def __str__(self):
    return json.dumps(self.conjug_info, indent=4)

def __bool__(self):
    return bool(self.conjug_info)

