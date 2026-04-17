from functools import partial
from typing import Optional, Sequence, Any

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline

from mlconjug3.feature_extractor import extract_verb_features


class Model:
    """
    Core ML model for verb template classification.
    """

    def __init__(
        self,
        vectorizer: Optional[Any] = None,
        classifier: Optional[Any] = None,
        language: Optional[str] = None,
    ) -> None:

        self.language = language

        # --------------------------
        # VECTORISER
        # --------------------------
        if vectorizer is None:
            vectorizer = CountVectorizer(
                analyzer=partial(
                    extract_verb_features,
                    lang=language,
                ),
                binary=True,
                lowercase=False,
            )

        # --------------------------
        # CLASSIFIER
        # --------------------------
        if classifier is None:
            classifier = SGDClassifier(
                loss="log_loss",
                penalty="elasticnet",
                l1_ratio=0.15,
                alpha=3e-6,
                max_iter=4000,
                tol=1e-4,
                early_stopping=False,
                n_iter_no_change=10,
                random_state=42,
            )

        # --------------------------
        # PIPELINE (MUST ALWAYS EXIST)
        # --------------------------
        self.pipeline = Pipeline([
            ("vectorizer", vectorizer),
            ("classifier", classifier),
        ])

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(language={self.language})"

    def train(self, samples: Sequence[str], labels: Sequence[int], sample_weight=None) -> "Model":
        """
        Safe training wrapper.
        """
        if sample_weight is not None:
            self.pipeline.fit(samples, labels, classifier__sample_weight=sample_weight)
        else:
            self.pipeline.fit(samples, labels)

        return self

    def predict(self, verbs: Sequence[str]):
        return self.pipeline.predict(verbs)

    def predict_proba(self, verbs: Sequence[str]):
        if hasattr(self.pipeline, "predict_proba"):
            return self.pipeline.predict_proba(verbs)
        raise AttributeError("Classifier does not support predict_proba")
