"""
This module declares the Model class.
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
    Manages the scikit-learn pipeline.
    """

    def __init__(
        self, vectorizer=None, feature_selector=None, classifier=None, language=None
    ):
        # ---------------------------
        # Vectorizer
        # ---------------------------
        if not vectorizer:
            tokenizer = partial(extract_verb_features, lang=language)

            vectorizer = CountVectorizer(
                analyzer="word",
                tokenizer=tokenizer,
                token_pattern=None,  # IMPORTANT: disables default regex tokenizer
                ngram_range=(2, 7),
                binary=True,
                lowercase=False,
            )

        # ---------------------------
        # Feature selector
        # ---------------------------
        if not feature_selector:
            feature_selector = SelectFromModel(
                LinearSVC(
                    penalty="l1",
                    max_iter=12000,
                    dual=False,
                    verbose=2,
                )
            )

        # ---------------------------
        # Classifier
        # ---------------------------
        if not classifier:
            classifier = SGDClassifier(
                loss="log_loss",
                penalty="elasticnet",
                l1_ratio=0.15,
                max_iter=4000,
                alpha=1e-5,
                random_state=42,
                verbose=2,
            )

        # ---------------------------
        # Pipeline
        # ---------------------------
        self.pipeline = Pipeline(
            [
                ("vectorizer", vectorizer),
                ("feature_selector", feature_selector),
                ("classifier", classifier),
            ]
        )

        self.language = language

    def __repr__(self):
        return "{}.{}({}, {}, {})".format(
            __name__, self.__class__.__name__, *sorted(self.pipeline.named_steps)
        )

    def train(self, samples, labels):
        """
        Train the pipeline.
        """
        self.pipeline = self.pipeline.fit(samples, labels)

    def predict(self, verbs):
        """
        Predict conjugation class.
        """
        return self.pipeline.predict(verbs)


if __name__ == "__main__":
    pass
