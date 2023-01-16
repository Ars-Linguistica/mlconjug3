import numpy as np
from sklearn.base import TransformerMixin, BaseEstimator
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline

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
                if self.language == 'fr':
                    morph_extractor = VerbMorphologyFr()
                elif self.language == 'en':
                    morph_extractor = VerbMorphologyEn()
                elif self.language == 'es':
                    morph_extractor = VerbMorphologyEs()
                elif self.language == 'it':
                    morph_extractor = VerbMorphologyIt()
                elif self.language == 'pt':
                    morph_extractor = VerbMorphologyPt()
                elif self.language == 'ro':
                    morph_extractor = VerbMorphologyRo()
                feature_vector.extend(morph_extractor.transform([verb]))
            
            features.append(feature_vector)
        return np.array(features)


class VerbMorphologyFr(TransformerMixin, BaseEstimator):
    """
    Transformer to extract morphological features of French verbs.

    Example use:
    from sklearn.pipeline import Pipeline
    from sklearn.linear_model import SGDClassifier
    from .VerbMorphologyFr import VerbMorphologyFr

    # Instantiate the morphological feature extractor
    morph_features = VerbMorphologyFr(root=True, suffix=True)

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


class VerbMorphologyEn(TransformerMixin, BaseEstimator):
    """
    Transformer to extract morphological features of English verbs.
    Example use:
    from sklearn.pipeline import Pipeline
    from sklearn.linear_model import SGDClassifier
    from .VerbMorphologyEn import VerbMorphologyEn
    
    # Instantiate the morphological feature extractor
    morph_features = VerbMorphologyEn(root=True, suffix=True)
    
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
    def __init__(self, root=True, suffix=True):
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


class VerbMorphologyEs(TransformerMixin, BaseEstimator):
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
    def init(self):
        pass
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        features = []
        for verb in X:
            feature_vector = []
            feature_vector.append(self.extract_verb_root(verb))
            feature_vector.append(self.extract_verb_suffix(verb))
            features.append(feature_vector)
        return np.array(features)
    
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


class VerbMorphologyIt(TransformerMixin, BaseEstimator):
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
    def __init__(self, root=True, suffix=True):
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


class VerbMorphologyPt(TransformerMixin, BaseEstimator):
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


class VerbMorphologyRo(TransformerMixin, BaseEstimator):
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

# Example usage:
# char_ngrams_pipe = Pipeline([
#     ('char_ngrams', TfidfVectorizer(analyzer='char', ngram_range=(3,5))),
# ])
# w2v_model = load_w2v_model('path/to/model')
# morph_features = ['root', 'suffix']
# feature_extractor = Pipeline([
#     ('features', VerbFeatures(char_ngrams_pipe, w2v_model, morph_features))
# ])
