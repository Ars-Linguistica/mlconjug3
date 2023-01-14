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

def __init__(self, language='fr'):
    if language not in _LANGUAGES:
        raise ValueError(_('Unsupported language.\nThe allowed languages are fr, en, es, it, pt, ro.'))
    self.language = language
    self.verbs = {}
    self.conjugations = OrderedDict()
    self._allowed_endings = self._detect_allowed_endings()
    self.cache = joblib.Memory(cachedir='/path/to/cache', verbose=0)

def __repr__(self):
    return '{0}.{1}(language={2})'.format(__name__, self.__class__.__name__, self.language)

def _load_verbs(self, verbs_file):
    """
    Load and parses the verbs from the json file.

    :param verbs_file: string or path object.
        Path to the verbs json file.

    """
    with open(verbs_file, 'r', encoding='utf-8') as file:
        self.verbs = json.load(file)
    return

def _load_conjugations(self, conjugations_file):
    """
    Load and parses the conjugations from the json file.

    :param conjugations_file: string or path object.
        Path to the conjugation json file.

    """
    with open(conjugations_file, 'r', encoding='utf-8') as file:
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
        return True
    return {verb.split(' ')[0][-2:] for verb in self.verbs if len(verb) >= 2}

def is_valid_verb(self, verb):
    """
    | Checks if the verb is a valid verb in the given language.
    | If the verb is invalid, returns False, otherwise returns the base form of the verb.

    :param verb: string.
        The verb to be checked.
    :return: string or bool.
        Returns the base form of the verb if valid, False otherwise.

    """
    if self.language == 'en':
        return verb
    base_form = self.verbs.get(verb, None)
    if not base_form:
    logger.warning("The verb '{}' is not a valid verb in the '{}' language.".format(verb, self.language))
    return None
    
        # Extract verb features
    X_verb = extract_verb_features(verb, self.language, (1, 2))

    # Predict conjugation template
    template = self.pipeline.predict(X_verb)[0]

    # Get conjugated forms
    conjugated_forms = self.conjugations[template]

    # Use cache if available
    cache_key = (verb, template)
    if cache_key in self.conjugation_cache:
        return self.conjugation_cache[cache_key]

    # Conjugate verb
    conjugated_verb_info = VerbInfo(verb, template, conjugated_forms)
    self.conjugation_cache[cache_key] = conjugated_verb_info

    return conjugated_verb_info

def conjugate(self, verb, subject='abbrev'):
    """
    | Conjugates a verb in the target language.

    :param verb: string.
        The infinitive form of the verb.
    :param subject: string.
        The format of the subject. The allowed values are: abbrev and pronoun.
        The default value is abbrev.

    :return: :class:`VerbInfo`.
        A VerbInfo object containing the base form, the template, and the conjugated forms of the verb.
    """
    if not verb:
        raise ValueError("A verb must be provided.")
    if subject not in ('abbrev', 'pronoun'):
        raise ValueError("The subject format must be 'abbrev' or 'pronoun'.")

    # Get base form and template
    base_form_template = self.is_valid_verb(verb)
    if base_form_template is None:
        return None

    # Get conjugated forms
    conjugated_forms = base_form_template.conjug_info

    # Filter conjugated forms by subject
    filtered_conjugated_forms = defaultdict(list)
    for subject_type, forms in conjugated_forms.items():
        if subject_type == subject or subject_type == 'both':
            for form in forms:
                filtered_conjugated_forms[form.tense].append(form)

    return VerbInfo(base_form_template.base_form, base_form_template.template, filtered_conjugated_forms)

