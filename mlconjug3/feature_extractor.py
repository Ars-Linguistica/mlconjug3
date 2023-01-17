from sklearn.base import BaseEstimator, TransformerMixin
from .verbs import *
from .constants import *
from .utils import logger

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
                    'ro': VerbMorphologyRo(),
                    'ar': ArabicVerbMorphology(), # added support for Arabic
                    'zh': ChineseVerbMorphology() # added support for Chinese
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
        :param lang: string. Language to analyze.
        :param ngram_range: tuple. Range of n-grams to extract.
            :return: list.
        List of extracted verb features.
    """
        verb_endings = []
        verb_starts = []
        length = len(verb)
        vowels = sum(1 for char in verb if char in 'aeiou')
        consonants = sum(1 for char in verb if char not in 'aeiou')
        
        # Extract verb endings and starting n-grams
        if lang == 'fr':
            # French verb inflection patterns
            verb_endings = [verb[-n:] for n in range(ngram_range[0], ngram_range[1]+1)]
            verb_starts = [verb[:n] for n in range(ngram_range[0], ngram_range[1]+1)]
        elif lang == 'ar':
            # Arabic verb inflection patterns
            pass # add code to extract arabic verb endings
        elif lang == 'ch':
            # Chinese verb inflection patterns
            pass # add code to extract chinese verb endings
        else:
            pass # add code to handle other languages inflection patterns
        
        # Other features
        features = verb_endings + verb_starts + [length, vowels, consonants, vowels/consonants if consonants else 0]
        return features

