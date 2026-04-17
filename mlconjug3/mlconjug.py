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
import pkg_resources


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
    Main class for conjugation using Verbiste + ML fallback.
    """

    def __init__(self, language="fr", model=None):
        self.language = language
        self.conjug_manager = Verbiste(language=language)

        if not model:
            with ZipFile(
                pkg_resources.resource_stream(
                    RESOURCE_PACKAGE, PRE_TRAINED_MODEL_PATH[language]
                )
            ) as content:
                with content.open(
                    f"trained_model-{self.language}-final.pickle", "r"
                ) as archive:
                    model = joblib.load(archive)

        self.model = model if model else None

    def __repr__(self):
        return f"{__name__}.{self.__class__.__name__}(language={self.language})"

    def conjugate(self, verbs, subject="abbrev"):
        if isinstance(verbs, str):
            return self._conjugate(verbs, subject)

        with ProcessPoolExecutor() as executor:
            return list(
                executor.map(self._conjugate, verbs, [subject] * len(verbs))
            )

    @lru_cache(maxsize=1024)
    def _conjugate(self, verb, subject="abbrev"):
        verb = verb.lower()

        # ----------------------------
        # 1. Try Verbiste (known verbs)
        # ----------------------------
        if verb in self.conjug_manager.verbs:
            verb_info = self.conjug_manager.get_verb_info(verb)
            conjug_info = self.conjug_manager.get_conjug_info(verb_info.template)

            if verb_info is None or conjug_info is None:
                return None

            return VERBS[self.language](verb_info, conjug_info, subject)

        # ----------------------------
        # 2. Unknown verb → ML fallback
        # ----------------------------
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

        # ML prediction path (this is critical for words like "cacater")
        prediction = self.model.predict([verb])[0]

        try:
            prediction_score = self.model.pipeline.predict_proba([verb])[0][prediction]
        except Exception:
            prediction_score = 0.0

        template = self.conjug_manager.templates[prediction]

        # root extraction (same logic as before, preserved)
        index = -len(template[template.index(":") + 1 :])
        root = verb if index == 0 else verb[:index]

        verb_info = VerbInfo(verb, root, template)
        conjug_info = self.conjug_manager.get_conjug_info(template)

        verb_object = VERBS[self.language](verb_info, conjug_info, subject)
        verb_object.confidence_score = round(prediction_score, 3)

        return verb_object

    def set_model(self, model):
        if not isinstance(model, Model):
            logger.warning(
                _("Please provide an instance of a mlconjug3.mlconjug3.Model")
            )
            raise ValueError("Invalid model type")

        self.model = model
