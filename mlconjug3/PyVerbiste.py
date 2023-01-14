# -*- coding: utf-8 -*-

"""
PyVerbiste.

| A Python library for conjugating verbs in French, English, Spanish, Italian, Portuguese and Romanian (more soon).
| It contains conjugation data generated by machine learning models using the python library mlconjug3.
| More information about mlconjug3 at https://pypi.org/project/mlconjug3/


| The conjugation data conforms to the XML schema defined by Verbiste.
| More information on Verbiste at https://perso.b2b2c.ca/~sarrazip/dev/conjug_manager.html

"""

__author__ = 'SekouDiaoNlp'
__author_email__ = 'diao.sekou.nlp@gmail.com'


import copy
import defusedxml.ElementTree as ET
import json
from collections import OrderedDict
import pkg_resources
from .verbs import *
from .constants import *
from .conjug_manager import ConjugManager


class Verbiste(ConjugManager):
    """
    This is the class handling the Verbiste xml files.

    :param language: string.
        | The language of the conjugator. The default value is fr for French.
        | The allowed values are: fr, en, es, it, pt, ro.
    :ivar language: Language of the conjugator.
    :ivar verbs: Dictionary where the keys are verbs and the values are conjugation patterns.
    :ivar conjugations: Dictionary where the keys are conjugation patterns and the values are inflected forms.

    """

    def _load_verbs(self, verbs_file):
        """
        Load and parses the verbs from the xml file.

        :param verbs_file: string or path object.
            Path to the verbs xml file.

        """
        self.verbs = self._parse_verbs(verbs_file.replace('json', 'xml'))
        return

    @staticmethod
    def _parse_verbs(file):
        """
        Parses the XML file.

        :param file: FileObject.
            XML file containing the verbs.
        :return: OrderedDict.
            An OrderedDict containing the verb and its template for all verbs in the file.

        """
        verbs_dic = {}
        xml = ET.parse(file)
        for verb in xml.findall("v"):
            verb_name = verb.find("i").text
            template = verb.find("t").text
            index = - len(template[template.index(":") + 1:])
            root = verb_name if index == 0 else verb_name[:index]
            verbs_dic[verb_name] = {"template": template, "root": root}
        return verbs_dic

    def _load_conjugations(self, conjugations_file):
        """
        Load and parses the conjugations from the xml file.

        :param conjugations_file: string or path object.
            Path to the conjugation xml file.

        """
        self.conjugations = self._parse_conjugations(conjugations_file.replace('json', 'xml'))
        return

    def _parse_conjugations(self, file):
        """
        Parses the XML file.

        :param file: FileObject.
            XML file containing the conjugation templates.
        :return: OrderedDict.
            An OrderedDict containing all the conjugation templates in the file.

        """
        conjugations_dic = {}
        xml = ET.parse(file)
        for template in xml.findall("template"):
            template_name = template.get("name")
            conjugations_dic[template_name] = OrderedDict()
            for mood in list(template):
                conjugations_dic[template_name][mood.tag] = OrderedDict()
                for tense in list(mood):
                    conjugations_dic[template_name][mood.tag][tense.tag.replace('-', ' ')] = self._load_tense(tense)
        return conjugations_dic

    @staticmethod
    def _load_tense(tense):
        """
        Load and parses the inflected forms of the tense from xml file.

        :param tense: list of xml tags containing inflected forms.
            The list of inflected forms for the current tense being processed.
        :return: list.
            List of inflected forms.

        """
        persons = list(tense)
        if not persons:
            return None
        elif len(persons) == 1:
            if persons[0].find("i") is None:
                return None
            conjug = persons[0].find("i").text
        else:
            conjug = []
            for pers, term in enumerate(persons):
                if term.find("i") is not None:
                    if term.find("i").text is not None:
                        conjug.append((pers, term.find("i").text))
                    else:
                        conjug.append((pers, ''))
                else:
                    conjug.append((pers, None))
        return conjug


if __name__ == "__main__":
    pass
