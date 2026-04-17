from functools import partial
from typing import Optional, Sequence, Any

import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.naive_bayes import ComplementNB
from sklearn.pipeline import Pipeline, FeatureUnion

from mlconjug3.feature_extractor import extract_verb_features


class Model:
    """
    Improved hybrid ensemble:

    - SGD: global linear boundary
    - NB: strong morphological sparse model
    - Weighted probability fusion (FIXED)
    """

    def __init__(
        self,
        vectorizer: Optional[Any] = None,
        classifier: Optional[Any] = None,
        language: Optional[str] = None,
    ) -> None:
        self.language = language

        weak = language in {"ro", "it"}

        char_vectorizer = CountVectorizer(
            analyzer="char",
            ngram_range=(2, 7 if weak else 6),
            lowercase=True,
        )

        linguistic_vectorizer = CountVectorizer(
            analyzer=partial(
                extract_verb_features,
                lang=language,
            ),
            lowercase=False,
        )

        self.vectorizer = FeatureUnion([
            ("char", char_vectorizer),
            ("linguistic", linguistic_vectorizer),
        ])

        # --------------------------
        # MODELS
        # --------------------------
        self.sgd = SGDClassifier(
            loss="log_loss",
            penalty="elasticnet",
            alpha=3e-6,
            l1_ratio=0.15,
            max_iter=4000,
            random_state=42,
        )

        self.nb = ComplementNB(alpha=0.7)

        self.pipeline_sgd = Pipeline([
            ("features", self.vectorizer),
            ("clf", self.sgd),
        ])

        self.pipeline_nb = Pipeline([
            ("features", self.vectorizer),
            ("clf", self.nb),
        ])

        # weights (tuned per language group)
        self.w_sgd = 0.6
        self.w_nb = 0.4 if weak else 0.3

    def train(self, samples: Sequence[str], labels: Sequence[int]) -> "Model":
        self.pipeline_sgd.fit(samples, labels)
        self.pipeline_nb.fit(samples, labels)
        return self

    def predict(self, verbs: Sequence[str]):
        proba_sgd = self.pipeline_sgd.predict_proba(verbs)
        proba_nb = self.pipeline_nb.predict_proba(verbs)

        # weighted fusion
        proba = (self.w_sgd * proba_sgd) + (self.w_nb * proba_nb)

        return np.argmax(proba, axis=1)

    def predict_proba(self, verbs: Sequence[str]):
        if hasattr(self.sgd, "predict_proba"):
            return self.pipeline_sgd.predict_proba(verbs)
        raise AttributeError("Classifier does not support predict_proba")
