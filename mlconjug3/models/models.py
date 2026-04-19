"""
models.py

Defines the core machine learning model used for verb conjugation.
"""

from functools import partial
from typing import Optional, Sequence, Any

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline

from mlconjug3.feature_extractor import extract_verb_features


class Model:
    """
    Machine learning model for verb template classification.

    This class wraps a scikit-learn Pipeline composed of:
    - A feature extractor (CountVectorizer with custom analyzer)
    - A classifier (SGDClassifier by default)
    """

    def __init__(
        self,
        vectorizer: Optional[Any] = None,
        classifier: Optional[Any] = None,
        language: Optional[str] = None,
    ) -> None:
        """
        Initialize the Model.

        Parameters
        ----------
        vectorizer : sklearn-compatible transformer, optional
            Feature extraction component used to convert verbs into feature vectors.
        classifier : sklearn-compatible estimator, optional
            Classification model used to predict verb templates.
        language : str, optional
            Language code used for feature extraction rules.
        """

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
        # PIPELINE
        # --------------------------
        self.pipeline = Pipeline([
            ("vectorizer", vectorizer),
            ("classifier", classifier),
        ])

    def __repr__(self) -> str:
        """
        Return string representation of the Model.

        Returns
        -------
        str
            Debug representation including language.
        """
        return f"{self.__class__.__name__}(language={self.language})"

    def train(
        self,
        samples: Sequence[str],
        labels: Sequence[int],
        sample_weight=None
    ) -> "Model":
        """
        Train the model on labeled verb data.

        Parameters
        ----------
        samples : Sequence[str]
            Input verb strings used for training.
        labels : Sequence[int]
            Target template indices.
        sample_weight : array-like, optional
            Optional weights for each training sample.

        Returns
        -------
        Model
            Trained model instance.
        """
        if sample_weight is not None:
            self.pipeline.fit(
                samples,
                labels,
                classifier__sample_weight=sample_weight
            )
        else:
            self.pipeline.fit(samples, labels)

        return self

    def predict(self, verbs: Sequence[str]):
        """
        Predict conjugation template indices for input verbs.

        Parameters
        ----------
        verbs : Sequence[str]
            Input verbs.

        Returns
        -------
        ndarray
            Predicted template indices (shape: [n_samples]).
        """
        return self.pipeline.predict(verbs)

    def predict_proba(self, verbs: Sequence[str]):
        """
        Predict probability distribution over conjugation templates.

        Parameters
        ----------
        verbs : Sequence[str]
            Input verbs.

        Returns
        -------
        ndarray
            Probability matrix of shape (n_samples, n_classes).

        Raises
        ------
        AttributeError
            If the classifier does not support probability prediction.
        """
        if hasattr(self.pipeline, "predict_proba"):
            return self.pipeline.predict_proba(verbs)
        raise AttributeError("Classifier does not support predict_proba")
