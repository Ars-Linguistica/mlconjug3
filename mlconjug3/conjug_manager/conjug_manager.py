"""
Conjugation manager module for mlconjug3.

This module defines the ConjugManager class, responsible for loading,
caching, and managing verb and conjugation data.

It serves as the bridge between raw dataset resources (JSON files)
and the higher-level conjugation logic used by the library.
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
    Manager for verb and conjugation data.

    This class loads verb lexicons and conjugation templates from JSON
    resources and provides access utilities for conjugation lookup.

    Parameters
    ----------
    language : str, default="default"
        Target language code. If "default", falls back to French ("fr").

    Attributes
    ----------
    language : str
        Active language used by the manager.
    verbs : dict
        Dictionary of verbs and their metadata.
    conjugations : OrderedDict
        Mapping of conjugation templates to tense structures.
    templates : list of str
        Sorted list of available conjugation templates.
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
        """
        String representation of the ConjugManager.
        """
        return f"{__name__}.{self.__class__.__name__}(language={self.language})"

    # ---------------------------
    # Resource helpers
    # ---------------------------

    def _is_real_file(self, path):
        """
        Check whether a path points to a real filesystem file.

        Parameters
        ----------
        path : str
            File path to check.

        Returns
        -------
        bool
            True if file exists on filesystem, False otherwise.
        """
        try:
            return os.path.isfile(path)
        except Exception:
            return False

    def _open_resource(self, relative_path):
        """
        Open a package resource in a zip-safe manner.

        Parameters
        ----------
        relative_path : str
            Path relative to the package resources.

        Returns
        -------
        file-like object
            Opened resource stream.
        """
        return resources.files(RESOURCE_PACKAGE).joinpath(relative_path).open(
            "r", encoding="utf-8"
        )

    # ---------------------------
    # Cache handling
    # ---------------------------

    def _load_cache(self, file):
        """
        Load cached version of a resource if available.

        Parameters
        ----------
        file : str
            Path to resource file.

        Returns
        -------
        object or None
            Cached data if valid cache exists, otherwise None.
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
        Save data to cache if filesystem write is possible.

        Parameters
        ----------
        file : str
            Original resource file path.
        data : object
            Data to cache.
        """
        if not self._is_real_file(file):
            return

        try:
            joblib.dump(data, file + ".pkl", compress=("gzip", 3))
        except Exception:
            pass  # safe fallback for read-only or zip environments

    # ---------------------------
    # Loaders
    # ---------------------------

    def _load_verbs(self, verbs_file):
        """
        Load verb dictionary from JSON resource.

        Parameters
        ----------
        verbs_file : str
            Path to verbs JSON resource.
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
        Load conjugation templates from JSON resource.

        Parameters
        ----------
        conjugations_file : str
            Path to conjugation templates JSON resource.
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
        Compute allowed verb endings for filtering.

        Returns
        -------
        set
            Set of valid verb suffixes for the current language.
        """
        if self.language == "en":
            return set()

        return {
            verb.split(" ")[0][-2:]
            for verb in self.verbs
            if len(verb) >= 2
        }

    def is_valid_verb(self, verb):
        """
        Check whether a verb is valid for the current language rules.

        Parameters
        ----------
        verb : str
            Verb to validate.

        Returns
        -------
        bool
            True if verb is valid, False otherwise.
        """
        if self.language == "en":
            return True
        return verb[-2:] in self._allowed_endings

    def get_verb_info(self, verb):
        """
        Retrieve metadata for a verb.

        Parameters
        ----------
        verb : str
            Verb to look up.

        Returns
        -------
        VerbInfo or None
            VerbInfo object if verb exists, otherwise None.
        """
        if verb not in self.verbs:
            return None

        data = self.verbs[verb]
        return VerbInfo(verb, data["root"], data["template"])

    def get_conjug_info(self, template):
        """
        Retrieve conjugation structure for a template.

        Parameters
        ----------
        template : str
            Conjugation template identifier.

        Returns
        -------
        dict or None
            Deep copy of conjugation structure, or None if not found.
        """
        if template not in self.conjugations:
            return None
        return copy.deepcopy(self.conjugations[template])


if __name__ == "__main__":
    pass
