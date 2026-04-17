"""
PyVerbiste.

Handles Verbiste XML data.
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
    Handles Verbiste XML files.
    """

    def _is_real_file(self, path):
        """
        Check if path is a real filesystem path (not from zip).
        """
        try:
            return os.path.isfile(path)
        except Exception:
            return False

    def _load_cache(self, file):
        """
        Load cache only if file is a real filesystem path.
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
        Save cache only if file is writable on filesystem.
        """
        if not self._is_real_file(file):
            return

        try:
            joblib.dump(data, file + ".pkl", compress=("gzip", 3))
        except Exception:
            pass  # fail silently (important for zip environments)

    def _open_resource(self, relative_path):
        """
        Open a resource in a zip-safe way.
        """
        return resources.files(RESOURCE_PACKAGE).joinpath(relative_path).open("rb")

    def _load_verbs(self, verbs_file):
        """
        Load verbs from XML resource.
        """
        xml_file = verbs_file.replace("json", "xml")
        self.verbs = self._parse_verbs(xml_file)

    def _parse_verbs(self, file):
        """
        Parse verbs XML.
        """
        cache = self._load_cache(file)
        if cache:
            return cache

        verbs_dic = {}

        # Try filesystem first, fallback to package resource
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
        Load conjugations from XML resource.
        """
        xml_file = conjugations_file.replace("json", "xml")
        self.conjugations = self._parse_conjugations(xml_file)

    def _parse_conjugations(self, file):
        """
        Parse conjugation templates XML.
        """
        cache = self._load_cache(file)
        if cache:
            return cache

        conjugations_dic = {}

        # Try filesystem first, fallback to package resource
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
        Parse tense inflections.
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
