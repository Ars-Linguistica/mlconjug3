from sklearn.base import BaseEstimator, TransformerMixin


class VerbFeatures(TransformerMixin, BaseEstimator):
    """
    Transformer to extract verb features using multiple techniques:
    - Character n-grams
    - Word2Vec embeddings
    - Morphological features
    """

    def __init__(self, char_ngrams=None, w2v_model=None, morph_features=None, language='fr'):
        self.char_ngrams = char_ngrams
        self.w2v_model = w2v_model
        self.morph_features = morph_features
        self.language = language

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        features = []
        for verb in X:
            feature_vector = []
            
            # Use custom vectorizer
            feature_vector.extend(VerbFeatures.extract_verb_features(verb, self.language, (2, 7)))

            # Extract character n-grams
            if self.char_ngrams:
                char_ngrams = [verb[i:i+n] for n in self.char_ngrams for i in range(len(verb)-n+1)]
                feature_vector.extend(char_ngrams)

            # Extract Word2Vec embeddings
            if self.w2v_model:
                try:
                    embeddings = self.w2v_model[verb]
                    feature_vector.extend(embeddings)
                except KeyError:
                    pass

            # Extract morphological features
            if self.morph_features:
                morph_extractor = {
                    'fr': VerbMorphologyFr(),
                    'en': VerbMorphologyEn(),
                    'es': VerbMorphologyEs(),
                    'it': VerbMorphologyIt(),
                    'pt': VerbMorphologyPt(),
                    'ro': VerbMorphologyRo()
                }.get(self.language)
                feature_vector.extend(morph_extractor.transform([verb]))

            features.append(feature_vector)
        return np.array(features)
        
    @staticmethod   
    def extract_verb_features(verb, lang, ngram_range):
        """
        | Custom Vectorizer optimized for extracting verbs features.
        | As in Indo-European languages verbs are inflected by adding a morphological suffix,
         the vectorizer extracts verb endings and produces a vector representation of the verb with binary features.
        | To enhance the results of the feature extration, several other features have been included:
        | The features are the verb's ending n-grams, starting n-grams, length of the verb, number of vowels,
         number of consonants and the ratio of vowels over consonants.
        :param verb: string.
            Verb to vectorize.
        :param lang: string.
            Language to analyze.
        :param ngram_range: tuple.
            The range of the ngram sliding window.
        :return: list.
            List of the most salient features of the verb for the task of finding it's conjugation's class.
        """
        _white_spaces = re.compile(r"\s\s+")
        verb = _white_spaces.sub(" ", verb)
        verb = verb.lower()
        verb_len = len(verb)
        length_feature = 'LEN={0}'.format(str(verb_len))
        min_n, max_n = ngram_range
        final_ngrams = ['END={0}'.format(verb[-n:]) for n in range(min_n, min(max_n + 1, verb_len + 1))]
        initial_ngrams = ['START={0}'.format(verb[:n]) for n in range(min_n, min(max_n + 1, verb_len + 1))]
        if lang not in _ALPHABET:
            lang = 'en'  # We chose 'en' as the default alphabet because english is more standard, without accents or diactrics.
        vowels = sum(verb.count(c) for c in _ALPHABET[lang]['vowels'])
        vowels_number = 'VOW_NUM={0}'.format(vowels)
        consonants = sum(verb.count(c) for c in _ALPHABET[lang]['consonants'])
        consonants_number = 'CONS_NUM={0}'.format(consonants)
        if consonants == 0:
            vow_cons_ratio = 'V/C=N/A'
        else:
            vow_cons_ratio = 'V/C={0}'.format(round(vowels / consonants, 2))
        final_ngrams.extend(initial_ngrams)
        final_ngrams.extend((length_feature, vowels_number, consonants_number, vow_cons_ratio))
        return final_ngrams
    

class VerbMorphology(TransformerMixin, BaseEstimator):
    def __init__(self, root=False, suffix=False):
        self.root = root
        self.suffix = suffix

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        features = []
        for verb in X:
            feature_vector = []
            if self.root:
                feature_vector.append(self.extract_verb_root(verb))
            if self.suffix:
                feature_vector.append(self.extract_verb_suffix(verb))
            features.append(feature_vector)
        return np.array(features)

    
class VerbMorphologyFr(VerbMorphology):
    def extract_verb_root(self, verb):
        """
        This function takes in a verb and returns the root of the verb.
        The root of the verb is the base form of the verb, from which all other forms are derived.
        :param verb: string.
            The verb to extract the root from.
        :return: string.
            The root of the verb.
        """
        # Regular expression to match the root of the verb
        pattern = r"^(.*?)(?:er|ir|re)$"
        match = re.match(pattern, verb)
        if match:
            return match.group(1)
        return None

    def extract_verb_suffix(self, verb):
        """
        This function takes in a verb and returns the suffix of the verb.
        The suffix of the verb is the part of the verb that indicates the conjugation group.
        :param verb: string.
            The verb to extract the suffix from.
        :return: string.
            The suffix of the verb.
        """
        # Regular expression to match the suffix of the verb
        pattern = r"^.*?(er|ir|re)$"
        match = re.match(pattern, verb)
        if match:
            return match.group(1)
        return None


    
class VerbMorphologyEn(VerbMorphology):
    def extract_verb_root(self, verb):
        pass
    def extract_verb_suffix(self, verb):
        pass

class VerbMorphologyEs(VerbMorphology):
    """
    Transformer to extract morphological features of Spanish verbs.
    
    Example use:
    from sklearn.pipeline import Pipeline
    from sklearn.linear_model import SGDClassifier
    from .VerbMorphologyEs import VerbMorphologyEs
    
    # Instantiate the morphological feature extractor
    morph_features = VerbMorphologyEs(root=True, suffix=True)
    
    # Create a pipeline with the morphological feature extractor and a classifier
    pipe = Pipeline([
        ('morph_features', morph_features),
        ('classifier', SGDClassifier()),
    ])
    
    # Fit the pipeline to the training data
    pipe.fit(X_train, y_train)
    
    # Make predictions on the test data
    predictions = pipe.predict(X_test)
    
    """
    def extract_verb_root(self, verb):
        """
        This function takes in a verb and returns the root of the verb.
        The root of the verb is the base form of the verb, from which all other forms are derived.
        :param verb: string.
            The verb to extract the root from.
        :return: string.
            The root of the verb.
        """
        # Regular expression to match the root of the verb
        pattern = r"^(.*?)(?:ar|er|ir)$"
        match = re.match(pattern, verb)
        if match:
            return match.group(1)
        else:
            return verb
        
    def extract_verb_suffix(self, verb):
        """
        This function takes in a verb and returns the suffix of the verb.
        The suffix of the verb is the part of the verb that changes to indicate its grammatical function.
        :param verb: string.
            The verb to extract the suffix from.
        :return: string.
            The suffix of the verb.
        """
        # Regular expression to match the suffix of the verb
        pattern = r"^.*?(ar|er|ir)$"
        match = re.match(pattern, verb)
        if match:
            return match.group(1)
        else:
            return ""


class VerbMorphologyIt(VerbMorphology):
    """
    Transformer to extract morphological features of Italian verbs.
    Example use:
    from sklearn.pipeline import Pipeline
    from sklearn.linear_model import SGDClassifier
    from .VerbMorphologyIt import VerbMorphologyIt
    # Instantiate the morphological feature extractor
    morph_features = VerbMorphologyIt(root=True, suffix=True)
    # Create a pipeline with the morphological feature extractor and a classifier
    pipe = Pipeline([
        ('morph_features', morph_features),
        ('classifier', SGDClassifier()),
    ])
    # Fit the pipeline to the training data
    pipe.fit(X_train, y_train)
    # Make predictions on the test data
    predictions = pipe.predict(X_test)
    """
    def extract_verb_root(self, verb):
        """
        This function takes in a verb and returns the root of the verb.
        The root of the verb is the base form of the verb, from which all other forms are derived.
        :param verb: string.
            The verb to extract the root from.
        :return: string.
            The root of the verb.
        """
        # Regular expression to match the root of the verb
        pattern = r"^(.*?)(?:are|ere|ire)$"
        match = re.match(pattern, verb)
        if match:
            return match.group(1)
        return None

    def extract_verb_suffix(self, verb):
        """
        This function takes in a verb and returns the suffix of the verb.
        The suffix of the verb is the part that is added to the root to form different tenses, moods, etc.
        :param verb: string.
            The verb to extract the suffix from.
        :return: string.
            The suffix of the verb.
        """
        # Regular expression to match the suffix of the verb
        pattern = r"^.*?(?:are|ere|ire)$"
        match = re.match(pattern, verb)
        if match:
            return match.group(1)
        return None


class VerbMorphologyPt(VerbMorphology):
    """
    Transformer to extract morphological features of Portuguese verbs.
    Example use:
    from sklearn.pipeline import Pipeline
    from sklearn.linear_model import SGDClassifier
    from .VerbMorphologyPt import VerbMorphologyPt
    # Instantiate the morphological feature extractor
    morph_features = VerbMorphologyPt(root=True, suffix=True)
    # Create a pipeline with the morphological feature extractor and a classifier
    pipe = Pipeline([
        ('morph_features', morph_features),
        ('classifier', SGDClassifier()),
    ])
    # Fit the pipeline to the training data
    pipe.fit(X_train, y_train)
    # Make predictions on the test data
    predictions = pipe.predict(X_test)
    """
    def extract_verb_root(self, verb):
        """
        This function takes in a verb and returns the root of the verb.
        The root of the verb is the base form of the verb, from which all other forms are derived.
        :param verb: string.
            The verb to extract the root from.
        :return: string.
            The root of the verb.
        """
        # Regular expression to match the root of the verb
        pattern = r"^(.*?)(?:ar|er|ir)$"
        match = re.match(pattern, verb)
        if match:
            return match.group(1)
        return None

    def extract_verb_suffix(self, verb):
        """
        This function takes in a verb and returns the suffix of the verb.
        The suffix of the verb is the part of the verb that is added to the root to indicate its grammatical function.
        :param verb: string.
            The verb to extract the suffix from.
        :return: string.
            The suffix of the verb.
        """
        # Regular expression to match the suffix of the verb
        pattern = r"^.*?([ar|er|ir])$"
        match = re.match(pattern, verb)
        if match:
            return match.group(1)
        return None


class VerbMorphologyRo(VerbMorphology):
    """
    Example use:
    from sklearn.pipeline import Pipeline
    from sklearn.linear_model import SGDClassifier
    from .VerbMorphologyRo import VerbMorphologyRo
    
    # Instantiate the morphological feature extractor
    morph_features = VerbMorphologyRo(root=True, suffix=True)
    
    # Create a pipeline with the morphological feature extractor and a classifier
    pipe = Pipeline([
        ('morph_features', morph_features),
        ('classifier', SGDClassifier()),
    ])
    
    # Fit the pipeline to the training data
    pipe.fit(X_train, y_train)
    
    # Make predictions on the test data
    predictions = pipe.predict(X_test)
    
    """
    def extract_verb_root(self, verb):
        """
        This function takes in a verb and returns the root of the verb.
        The root of the verb is the base form of the verb, from which all other forms are derived.
        :param verb: string.
            The verb to extract the root from.
        :return: string.
            The root of the verb.
        """
        # Regular expression to match the root of the verb
        pattern = r"^(.*?)a$"
        match = re.match(pattern, verb)
        if match:
            return match.group(1)
        else:
            return None
    
    def extract_verb_suffix(self, verb):
        """
        This function takes in a verb and returns the suffix of the verb.
        :param verb: string.
            The verb to extract the suffix from.
        :return: string.
            The suffix of the verb.
        """
        # Regular expression to match the suffix of the verb
        pattern = r"^.*?(a)$"
        match = re.match(pattern, verb)
        if match:
            return match.group(1)
        else:
            return None

