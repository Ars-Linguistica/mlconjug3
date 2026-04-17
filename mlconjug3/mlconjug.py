"""
mlconjug3 Main module.

This module provides an easy-to-use interface for conjugating verbs using machine learning models.
...
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
from collections import defaultdict
from random import Random

import joblib
import re
from zipfile import ZipFile
from importlib import resources


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
    Main class of the project.
    """

    def __init__(self, language="fr", model=None):
        self.language = language
        self.conjug_manager = Verbiste(language=language)

        if model is None:
            model = self._load_default_model(language)

        if model:
            self.set_model(model)
        else:
            self.model = None

    def __repr__(self):
        return f"{__name__}.{self.__class__.__name__}(language={self.language})"

    def _load_default_model(self, language):
        """
        Load the pre-trained model in a fully zip-safe way.
        """
        try:
            model_resource = PRE_TRAINED_MODEL_PATH[language]
            model_filename = f"trained_model-{language}-final.pickle"

            with resources.files(RESOURCE_PACKAGE).joinpath(model_resource).open("rb") as model_stream:
                with ZipFile(model_stream) as zip_file:
                    with zip_file.open(model_filename) as archive:
                        return joblib.load(archive)

        except Exception as exc:
            logger.error(
                _("Failed to load pre-trained model for language '{0}': {1}").format(
                    language, exc
                )
            )
            return None

    def conjugate(self, verbs, subject="abbrev"):
        """
        Conjugate multiple verbs using multi-processing.
        """
        if isinstance(verbs, str):
            return self._conjugate(verbs, subject)

        with ProcessPoolExecutor() as executor:
            results = list(
                executor.map(self._conjugate, verbs, [subject] * len(verbs))
            )
        return results

    @lru_cache(maxsize=1024)
    def _conjugate(self, verb, subject="abbrev"):
        """
        Core conjugation logic.
        """
        verb = verb.lower()
        prediction_score = 0

        if not self.conjug_manager.is_valid_verb(verb):
            logger.warning(
                _("The supplied word: {0} is not a valid verb in {1}.").format(
                    verb, LANGUAGE_FULL[self.language]
                )
            )
            return None

        if verb not in self.conjug_manager.verbs:
            if self.model is None:
                logger.warning(
                    _("Please provide an instance of a mlconjug3.mlconjug3.Model")
                )
                logger.warning(
                    _(
                        "The supplied word: {0} is not in the conjugation {1} table and no Conjugation Model was provided."
                    ).format(verb, LANGUAGE_FULL[self.language])
                )
                return None

            prediction = self.model.predict([verb])[0]
            prediction_score = self.model.pipeline.predict_proba([verb])[0][prediction]

            template = self.conjug_manager.templates[prediction]
            index = -len(template[template.index(":") + 1 :])
            root = verb if index == 0 else verb[:index]

            verb_info = VerbInfo(verb, root, template)
            conjug_info = self.conjug_manager.get_conjug_info(template)

            verb_object = VERBS[self.language](
                verb_info, conjug_info, subject, predicted=True
            )
            verb_object.confidence_score = round(prediction_score, 3)

        else:
            verb_info = self.conjug_manager.get_verb_info(verb)
            if verb_info is None:
                return None

            conjug_info = self.conjug_manager.get_conjug_info(verb_info.template)
            if conjug_info is None:
                return None

            verb_object = VERBS[self.language](
                verb_info, conjug_info, subject
            )

        return verb_object

    def set_model(self, model):
        """
        Assign a trained model.
        """
        if not isinstance(model, Model):
            logger.warning(
                _("Please provide an instance of a mlconjug3.mlconjug3.Model")
            )
            raise ValueError
        self.model = model


if __name__ == "__main__":
    pass
