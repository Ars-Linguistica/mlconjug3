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
