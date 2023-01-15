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

    def __init__(self, char_ngrams=None, w2v_model=None, morph_features=None):
        self.char_ngrams = char_ngrams
        self.w2v_model = w2v_model
        self.morph_features = morph_features

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
                for feature in self.morph_features:
                    feature_vector.append(extract_morph_feature(verb, feature))
            
            features.append(feature_vector)
        return np.array(features)

def extract_morph_feature(verb, feature):
    """
    Function to extract specific morphological feature from a verb
    """
    if feature == 'root':
        # Extract root of the verb
        return extract_verb_root(verb)
    elif feature == 'suffix':
        # Extract suffix of the verb
        return extract_verb_suffix(verb)
    # Add other feature extraction methods as necessary
    return None


# ToDo: indent properly
class VerbMorphologyFr:
def extract_verb_root(verb):
    """
    This function takes in a verb and returns the root of the verb.
    The root of the verb is the base form of the verb, from which all other forms are derived.
    :param verb: string.
        The verb to extract the root from.
    :return: string.
        The root of the verb.
    """
    # Regular expression to match the root of the verb
    pattern = r"^(.*?)(?:er|ir|re|[^aeiou]ir|[^aeiou]ir[^aeiou]ir)$"
    match = re.match(pattern, verb)
    if match:
        return match.group(1)
    else:
        return verb

def extract_verb_suffix(verb):
    """
    This function takes in a verb and returns the suffix of the verb.
    The suffix of the verb is the part of the verb that changes to indicate its grammatical function.
    :param verb: string.
        The verb to extract the suffix from.
    :return: string.
        The suffix of the verb.
    """
    # Regular expression to match the suffix of the verb
    pattern = r"^.*?(er|ir|re|[^aeiou]ir|[^aeiou]ir[^aeiou]ir)$"
    match = re.match(pattern, verb)
    if match:
        return match.group(1)
    else:
        return ""

# Example usage:
# char_ngrams_pipe = Pipeline([
#     ('char_ngrams', TfidfVectorizer(analyzer='char', ngram_range=(3,5))),
# ])
# w2v_model = load_w2v_model('path/to/model')
# morph_features = ['root', 'suffix']
# feature_extractor = Pipeline([
#     ('features', VerbFeatures(char_ngrams_pipe, w2v_model, morph_features))
# ])
