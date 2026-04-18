"""
PyVerbiste

Handles loading, parsing, and caching of Verbiste XML linguistic resources.
Provides filesystem-safe and package-resource-safe access to conjugation data.
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
    Verbiste backend implementation for parsing XML conjugation resources.

    This class extends ConjugManager and provides:
    - XML parsing of verb lexicons and conjugation templates
    - Optional disk caching via joblib
    - Zip-safe resource loading via importlib.resources
    """

    def _is_real_file(self, path):
        """
        Check whether a given path is a real filesystem path.

        Used to distinguish between:
        - Local filesystem files
        - Package-embedded resources (zip/importlib)

        :param path: File path to check
        :type path: str
        :return: True if path exists on filesystem, False otherwise
        :rtype: bool
        """
        try:
            return os.path.isfile(path)
        except Exception:
            return False

    def _load_cache(self, file):
        """
        Load cached parsed XML data if available and valid.

        Cache is only used when:
        - File is on filesystem
        - File has a corresponding `.pkl` cache
        - Cache is newer than source XML

        :param file: Path to XML file
        :type file: str
        :return: Cached data or None if unavailable
        :rtype: dict | None
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
        Save parsed data to cache file.

        Cache is only written when:
        - File exists on filesystem
        - Write permissions are available

        Failures are silently ignored (safe for zip/package environments).

        :param file: Original XML file path
        :type file: str
        :param data: Parsed data to cache
        :type data: dict
        """
        if not self._is_real_file(file):
            return

        try:
            joblib.dump(data, file + ".pkl", compress=("gzip", 3))
        except Exception:
            pass

    def _open_resource(self, relative_path):
        """
        Open a package resource in a filesystem-agnostic way.

        Supports both installed packages and zipped distributions.

        :param relative_path: Relative path inside package
        :type relative_path: str
        :return: Binary file-like object
        :rtype: BinaryIO
        """
        return resources.files(RESOURCE_PACKAGE).joinpath(relative_path).open("rb")

    def _load_verbs(self, verbs_file):
        """
        Load verb lexicon from XML source.

        :param verbs_file: Path to verbs resource (XML or logical name)
        :type verbs_file: str
        """
        xml_file = verbs_file.replace("json", "xml")
        self.verbs = self._parse_verbs(xml_file)

    def _parse_verbs(self, file):
        """
        Parse verb lexicon XML into a structured dictionary.

        Uses cache when available.

        :param file: Path to XML file or resource
        :type file: str
        :return: Dictionary mapping verbs to root and template info
        :rtype: dict
        """
        cache = self._load_cache(file)
        if cache:
            return cache

        verbs_dic = {}

        if self._is_real_file(file):
            xml = ET.parse(file)
        else:
            with self._open_resource(file) as f:
                xml = ET.parse(f)

        for verb in xml.findall("v"):
            verb_name = verb.find("i").text
            template = verb.find("t").text
            index = -len(template[template.index(":") + 1 :])
            root = verb_name if index == 0 else verb_name[:index]
            verbs_dic[verb_name] = {"template": template, "root": root}

        self._save_cache(file, verbs_dic)
        return verbs_dic

    def _load_conjugations(self, conjugations_file):
        """
        Load conjugation templates from XML source.

        :param conjugations_file: Path to conjugation XML resource
        :type conjugations_file: str
        """
        xml_file = conjugations_file.replace("json", "xml")
        self.conjugations = self._parse_conjugations(xml_file)

    def _parse_conjugations(self, file):
        """
        Parse conjugation template XML into structured dictionary.

        Uses cache when available.

        :param file: Path to XML file or resource
        :type file: str
        :return: Nested dictionary of conjugation templates
        :rtype: dict
        """
        cache = self._load_cache(file)
        if cache:
            return cache

        conjugations_dic = {}

        if self._is_real_file(file):
            xml = ET.parse(file)
        else:
            with self._open_resource(file) as f:
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

    @staticmethod
    def _load_tense(tense):
        """
        Convert XML tense node into structured conjugation data.

        :param tense: XML tense node
        :type tense: xml.etree.ElementTree.Element
        :return: Either a string, list of (person, form), or None
        :rtype: str | list[tuple[int, str]] | None
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
