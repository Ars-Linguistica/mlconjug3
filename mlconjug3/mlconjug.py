"""
mlconjug.py

Main entry point for verb conjugation using a hybrid approach:
- Rule-based conjugation via Verbiste for known verbs
- Machine learning fallback for unknown verbs

This module exposes the `Conjugator` class.
"""

from .PyVerbiste import Verbiste
from .conjug_manager import ConjugManager
from .constants import *
from .verbs import *
from .feature_extractor import extract_verb_features
from .dataset import DataSet
from .models import Model
from .utils import logger

from functools import lru_cache
from concurrent.futures import ProcessPoolExecutor
from zipfile import ZipFile
import joblib
from importlib import resources
import numpy as np


VERBS = {
    "fr": VerbFr,
    "en": VerbEn,
    "es": VerbEs,
    "it": VerbIt,
    "pt": VerbPt,
    "ro": VerbRo,
}


class Conjugator:
    """
    Main class for verb conjugation.

    Combines:
    - Verbiste dictionary-based conjugation
    - Machine learning fallback for unknown verbs
    """

    def __init__(self, language="fr", model=None):
        """
        Initialize the Conjugator.

        Parameters
        ----------
        language : str
            Target language.
        model : Model or estimator, optional
            A trained model. If None, a pre-trained model is loaded.
        """
        self.language = language
        self.conjug_manager = Verbiste(language=language)

        if model is None:
            resource_path = resources.files(RESOURCE_PACKAGE).joinpath(
                PRE_TRAINED_MODEL_PATH[language]
            )

            with resource_path.open("rb") as stream:
                with ZipFile(stream) as content:
                    with content.open(
                        f"trained_model-{self.language}-final.pickle"
                    ) as archive:
                        model = joblib.load(archive)

            self.set_model(model)
        else:
            if isinstance(model, Model):
                self.set_model(model)
            else:
                logger.warning(
                    _("Using a non-Model estimator. Compatibility is not guaranteed.")
                )
                self.model = model

    def __repr__(self):
        """
        String representation of the Conjugator.
        """
        return f"{__name__}.{self.__class__.__name__}(language={self.language})"

    def conjugate(self, verbs, subject="abbrev"):
        """
        Conjugate one or multiple verbs.
        """
        if isinstance(verbs, str):
            return self._conjugate(verbs, subject)

        with ProcessPoolExecutor() as executor:
            return list(
                executor.map(self._conjugate, verbs, [subject] * len(verbs))
            )

    @lru_cache(maxsize=1024)
    def _conjugate(self, verb, subject="abbrev"):
        """
        Internal conjugation logic.
        """
        verb = verb.lower()

        # Known verb
        if verb in self.conjug_manager.verbs:
            verb_info = self.conjug_manager.get_verb_info(verb)
            conjug_info = self.conjug_manager.get_conjug_info(verb_info.template)

            if verb_info is None or conjug_info is None:
                return None

            return VERBS[self.language](verb_info, conjug_info, subject)

        # ML fallback
        if self.model is None:
            logger.warning(
                _("Please provide an instance of a mlconjug3.mlconjug3.Model")
            )
            return None

        prediction = self.model.predict([verb])[0]

        template = None
        confidence_score = None

        # support numpy integers
        if isinstance(prediction, (int, np.integer)):
            try:
                template = self.conjug_manager.templates[int(prediction)]
            except Exception:
                raise ValueError(
                    f"Invalid template index predicted: {prediction}"
                )

        elif isinstance(prediction, str):
            template = prediction

        else:
            raise ValueError(
                f"Unsupported prediction type: {type(prediction)}"
            )

        # Probability handling
        try:
            if hasattr(self.model, "predict_proba"):
                proba = self.model.predict_proba([verb])[0]

                if hasattr(self.model, "pipeline"):
                    classes = self.model.pipeline.classes_
                elif hasattr(self.model, "classes_"):
                    classes = self.model.classes_
                else:
                    classes = None

                if classes is not None:
                    class_index = list(classes).index(prediction)
                    confidence_score = round(float(proba[class_index]), 3)

        except Exception:
            confidence_score = None

        # Build verb
        index = -len(template[template.index(":") + 1 :])
        root = verb if index == 0 else verb[:index]

        verb_info = VerbInfo(verb, root, template)
        conjug_info = self.conjug_manager.get_conjug_info(template)

        verb_object = VERBS[self.language](verb_info, conjug_info, subject)

        if confidence_score is not None:
            verb_object.confidence_score = confidence_score

        return verb_object

    def set_model(self, model):
        """
        Set the conjugation model.
        """
        if not isinstance(model, Model):
            logger.warning(
                _("Please provide an instance of a mlconjug3.mlconjug3.Model")
            )
            raise ValueError("Invalid model type")

        self.model = model
