"""
ConjugManager.

Handles mlconjug3 JSON conjugation data.
"""

__author__ = "Ars-Linguistica"
__author_email__ = "diao.sekou.nlp@gmail.com"

import os
import joblib
import copy
import json
from collections import OrderedDict
from importlib import resources

from mlconjug3.constants import *
from mlconjug3.verbs import *


class ConjugManager:
    """
    Handles mlconjug3 JSON files.
    """

    def __init__(self, language="default"):
        if language not in LANGUAGES:
            raise ValueError(
                _(
                    "Unsupported language.\nThe allowed languages are fr, en, es, it, pt, ro."
                )
            )

        self.language = "fr" if language == "default" else language
        self.verbs = {}
        self.conjugations = OrderedDict()

        verbs_file = VERBS_RESOURCE_PATH[self.language]
        self._load_verbs(verbs_file)

        self._allowed_endings = self._detect_allowed_endings()

        conjugations_file = CONJUGATIONS_RESOURCE_PATH[self.language]
        self._load_conjugations(conjugations_file)

        self.templates = sorted(self.conjugations.keys())

    def __repr__(self):
        return f"{__name__}.{self.__class__.__name__}(language={self.language})"

    # ---------------------------
    # Resource helpers
    # ---------------------------

    def _is_real_file(self, path):
        try:
            return os.path.isfile(path)
        except Exception:
            return False

    def _open_resource(self, relative_path):
        """
        Open a resource in a zip-safe way.
        """
        return resources.files(RESOURCE_PACKAGE).joinpath(relative_path).open(
            "r", encoding="utf-8"
        )

    # ---------------------------
    # Cache handling
    # ---------------------------

    def _load_cache(self, file):
        """
        Load cache only if file is a real filesystem path.
        """
        if not self._is_real_file(file):
            return None

        if not file.endswith(".json"):
            raise ValueError(f"Invalid file path, expected .json file, got {file}")

        pkl_file = file + ".pkl"

        if os.path.isfile(pkl_file):
            if os.path.getmtime(file) <= os.path.getmtime(pkl_file):
                return joblib.load(pkl_file)

        return None

    def _save_cache(self, file, data):
        """
        Save cache only if file is writable.
        """
        if not self._is_real_file(file):
            return

        try:
            joblib.dump(data, file + ".pkl", compress=("gzip", 3))
        except Exception:
            pass  # safe fallback

    # ---------------------------
    # Loaders
    # ---------------------------

    def _load_verbs(self, verbs_file):
        """
        Load verbs JSON.
        """
        cache = self._load_cache(verbs_file)
        if cache:
            self.verbs = cache
            return

        if self._is_real_file(verbs_file):
            with open(verbs_file, encoding="utf-8") as file:
                self.verbs = json.load(file)
        else:
            with self._open_resource(verbs_file) as file:
                self.verbs = json.load(file)

        self._save_cache(verbs_file, self.verbs)

    def _load_conjugations(self, conjugations_file):
        """
        Load conjugations JSON.
        """
        cache = self._load_cache(conjugations_file)
        if cache:
            self.conjugations = cache
            return

        if self._is_real_file(conjugations_file):
            with open(conjugations_file, encoding="utf-8") as file:
                self.conjugations = json.load(file)
        else:
            with self._open_resource(conjugations_file) as file:
                self.conjugations = json.load(file)

        self._save_cache(conjugations_file, self.conjugations)

    # ---------------------------
    # Logic
    # ---------------------------

    def _detect_allowed_endings(self):
        """
        Detect allowed verb endings.
        """
        if self.language == "en":
            return set()
        return {verb.split(" ")[0][-2:] for verb in self.verbs if len(verb) >= 2}

    def is_valid_verb(self, verb):
        """
        Check if verb is valid.
        """
        if self.language == "en":
            return True
        return verb[-2:] in self._allowed_endings

    def get_verb_info(self, verb):
        """
        Get VerbInfo.
        """
        if verb not in self.verbs:
            return None

        data = self.verbs[verb]
        return VerbInfo(verb, data["root"], data["template"])

    def get_conjug_info(self, template):
        """
        Get conjugation template.
        """
        if template not in self.conjugations:
            return None
        return copy.deepcopy(self.conjugations[template])


if __name__ == "__main__":
    pass
