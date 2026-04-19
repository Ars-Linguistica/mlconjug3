"""
PyVerbiste.

Handles Verbiste XML data and provides a lightweight rule-based
conjugation backend using XML templates.

This module supports both filesystem-based resources and packaged
resources (e.g., inside wheels or zip files), with optional caching
for performance.
"""

__author__ = "Ars-Linguistica"
__author_email__ = "diao.sekou.nlp@gmail.com"

import os
import joblib
import defusedxml.ElementTree as ET
from collections import OrderedDict
from importlib import resources

from mlconjug3.constants import *
from mlconjug3.verbs import *
from mlconjug3.conjug_manager import *


class Verbiste(ConjugManager):
    """
    Verbiste XML-based conjugation manager.

    This class loads verb definitions and conjugation templates from
    Verbiste XML resources. It supports:

    - Loading from filesystem or packaged resources
    - Transparent caching using joblib
    - Graceful fallback when resources are missing

    Inherits from:
        ConjugManager
    """

    # ---------------------------
    # File helpers
    # ---------------------------

    def _is_real_file(self, path):
        """
        Determine whether a given path refers to a real file
        on the local filesystem.

        Parameters
        ----------
        path : str
            File path to check.

        Returns
        -------
        bool
            True if the file exists on disk, False otherwise.
        """
        try:
            return os.path.isfile(path)
        except Exception:
            return False

    # ---------------------------
    # Cache handling
    # ---------------------------

    def _load_cache(self, file):
        """
        Load a cached version of parsed XML data if available.

        Cache is only used when the source file exists on disk and
        the cache file is newer than the source XML.

        Parameters
        ----------
        file : str
            Path to the XML file.

        Returns
        -------
        dict or None
            Cached data if valid, otherwise None.

        Raises
        ------
        ValueError
            If the file extension is not `.xml`.
        """
        if not self._is_real_file(file):
            return None

        if not file.endswith(".xml"):
            raise ValueError(f"Invalid file path, expected .xml file, got {file}")

        pkl_file = file + ".pkl"

        if os.path.isfile(pkl_file):
            if os.path.getmtime(file) <= os.path.getmtime(pkl_file):
                return joblib.load(pkl_file)

        return None

    def _save_cache(self, file, data):
        """
        Save parsed XML data to a cache file.

        Cache is only written when the file exists on disk and is writable.
        Failures are silently ignored (important for packaged environments).

        Parameters
        ----------
        file : str
            Original XML file path.
        data : dict
            Parsed data to cache.
        """
        if not self._is_real_file(file):
            return

        try:
            joblib.dump(data, file + ".pkl", compress=("gzip", 3))
        except Exception:
            pass  # Safe fallback for read-only or zip environments

    # ---------------------------
    # Resource handling
    # ---------------------------

    def _open_resource(self, relative_path):
        """
        Open a packaged resource in a zip-safe way.

        Parameters
        ----------
        relative_path : str
            Path relative to the package root.

        Returns
        -------
        file-like object or None
            Opened binary stream if resource exists, otherwise None.
        """
        try:
            return resources.files(RESOURCE_PACKAGE).joinpath(relative_path).open("rb")
        except (FileNotFoundError, ModuleNotFoundError):
            return None

    # ---------------------------
    # Verb loading
    # ---------------------------

    def _load_verbs(self, verbs_file):
        """
        Load verbs from an XML resource.

        Parameters
        ----------
        verbs_file : str
            Path to the verbs resource (JSON name will be converted to XML).

        Notes
        -----
        The method automatically converts `.json` paths to `.xml`
        to maintain compatibility with existing configuration.
        """
        xml_file = verbs_file.replace("json", "xml")
        self.verbs = self._parse_verbs(xml_file)

    def _parse_verbs(self, file):
        """
        Parse verbs from a Verbiste XML file.

        Parameters
        ----------
        file : str
            Path to the XML file.

        Returns
        -------
        dict
            Dictionary mapping verb names to their template and root.
        """
        cache = self._load_cache(file)
        if cache:
            return cache

        verbs_dic = {}

        # Load XML (filesystem or package resource)
        if self._is_real_file(file):
            xml = ET.parse(file)
        else:
            f = self._open_resource(file)
            if f is None:
                return {}  # Safe fallback
            with f:
                xml = ET.parse(f)

        for verb in xml.findall("v"):
            verb_name = verb.find("i").text
            template = verb.find("t").text
            index = -len(template[template.index(":") + 1 :])
            root = verb_name if index == 0 else verb_name[:index]
            verbs_dic[verb_name] = {"template": template, "root": root}

        self._save_cache(file, verbs_dic)
        return verbs_dic

    # ---------------------------
    # Conjugation loading
    # ---------------------------

    def _load_conjugations(self, conjugations_file):
        """
        Load conjugation templates from XML resource.

        Parameters
        ----------
        conjugations_file : str
            Path to the conjugation templates resource.
        """
        xml_file = conjugations_file.replace("json", "xml")
        self.conjugations = self._parse_conjugations(xml_file)

    def _parse_conjugations(self, file):
        """
        Parse conjugation templates from XML.

        Parameters
        ----------
        file : str
            Path to the XML file.

        Returns
        -------
        dict
            Nested dictionary of conjugation templates.
        """
        cache = self._load_cache(file)
        if cache:
            return cache

        conjugations_dic = {}

        # Load XML
        if self._is_real_file(file):
            xml = ET.parse(file)
        else:
            f = self._open_resource(file)
            if f is None:
                return {}
            with f:
                xml = ET.parse(f)

        for template in xml.findall("template"):
            template_name = template.get("name")
            conjugations_dic[template_name] = OrderedDict()

            for mood in list(template):
                conjugations_dic[template_name][mood.tag] = OrderedDict()

                for tense in list(mood):
                    conjugations_dic[template_name][mood.tag][
                        tense.tag.replace("-", " ")
                    ] = self._load_tense(tense)

        self._save_cache(file, conjugations_dic)
        return conjugations_dic

    # ---------------------------
    # Tense parsing
    # ---------------------------

    @staticmethod
    def _load_tense(tense):
        """
        Parse a tense node into conjugation forms.

        Parameters
        ----------
        tense : xml.etree.ElementTree.Element
            XML node representing a tense.

        Returns
        -------
        list or str or None
            - List of (person_index, form) tuples for multi-person tenses
            - String for single-form tenses
            - None if empty
        """
        persons = list(tense)

        if not persons:
            return None

        if len(persons) == 1:
            node = persons[0].find("i")
            return node.text if node is not None else None

        conjug = []
        for pers, term in enumerate(persons):
            node = term.find("i")
            if node is not None:
                conjug.append((pers, node.text or ""))
            else:
                conjug.append((pers, None))

        return conjug


if __name__ == "__main__":
    pass
