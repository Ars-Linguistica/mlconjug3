"""
This module declares the Model class.

It provides a Model class that wraps around scikit-learn's pipeline,
and offers a simple train, predict, and evaluate interface for training conjugation models.
The Model class also provides default values for the vectorizer, feature selector and classifier,
which work well for many languages and can be overridden as needed.
"""

from sklearn.feature_selection import SelectFromModel
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import LinearSVC
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline

from mlconjug3.constants import *

from mlconjug3.feature_extractor import extract_verb_features

from functools import partial


class Model:
    """
    | This class manages the scikit-learn pipeline.
    | The Pipeline includes a feature vectorizer, a feature selector and a classifier.
    | If any of the vectorizer, feature selector or classifier is not supplied at instance declaration,
     the __init__ method will provide good default values that get more than 92% prediction accuracy.
     
    :param vectorizer: scikit-learn Vectorizer.
    :param feature_selector: scikit-learn Classifier with a fit_transform() method
    :param classifier: scikit-learn Classifier with a predict() method
    :param language: Language of the corpus of verbs to be analyzed.
    :ivar pipeline: scikit-learn Pipeline Object.
    :ivar language: Language of the corpus of verbs to be analyzed.
    """

    def __init__(self, vectorizer=None, feature_selector=None, classifier=None, language=None):
        if not vectorizer:
            vectorizer = CountVectorizer(analyzer=partial(extract_verb_features, lang=language, ngram_range=(2, 7)),
                                         binary=True, lowercase=False)
        if not feature_selector:
            feature_selector = SelectFromModel(LinearSVC(penalty='l1', max_iter=12000, dual=False, verbose=2))
        if not classifier:
            classifier = SGDClassifier(loss='log_loss', penalty='elasticnet', l1_ratio=0.15,
                                       max_iter=4000, alpha=1e-5, random_state=42, verbose=2)
        self.pipeline = Pipeline([('vectorizer', vectorizer),
                                  ('feature_selector', feature_selector),
                                  ('classifier', classifier)])
        self.language = language
        return

    def __repr__(self):
        return '{}.{}({}, {}, {})'.format(__name__, self.__class__.__name__, *sorted(self.pipeline.named_steps))

    def train(self, samples, labels):
        """
        Trains the pipeline on the supplied samples and labels.
        
        :param samples: list.
            List of verbs.
        :param labels: list.
            List of verb templates.
        """
        self.pipeline = self.pipeline.fit(samples, labels)
        return

    def predict(self, verbs):
        """
        Predicts the conjugation class of the provided list of verbs.
        
        :param verbs: list.
            List of verbs.
        :return predictions: list.
            List of predicted conjugation groups.
        """
        return self.pipeline.predict(verbs)
      
if __name__ == "__main__":
    pass
