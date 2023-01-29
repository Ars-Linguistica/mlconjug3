"""
PyVerbiste.

This module contains the code for the class Vrbiste.
More information about mlconjug3 at https://pypi.org/project/mlconjug3/


The conjugation data conforms to the XML schema defined by Verbiste.
More information on Verbiste at https://perso.b2b2c.ca/~sarrazip/dev/conjug_manager.html

"""

__author__ = 'Ars-Linguistica'
__author_email__ = 'diao.sekou.nlp@gmail.com'


import os
import joblib
import copy
import defusedxml.ElementTree as ET
import json
from collections import OrderedDict
import pkg_resources
from mlconjug3.constants import *
from mlconjug3.verbs import *
from mlconjug3.conjug_manager import *


class Verbiste(ConjugManager):
    """
    This is the class handling the Verbiste xml files.

    :param language: string.
        | The language of the conjugator. The default value is fr for French.
        | The allowed values are: fr, en, es, it, pt, ro.
    :ivar language: Language of the conjugator.
    :ivar verbs: Dictionary where the keys are verbs and the values are conjugation patterns.
    :ivar conjugations: Dictionary where the keys are conjugation patterns and the values are inflected forms.
    :ivar _allowed_endings: set.
        | A set containing the allowed endings of verbs in the target language.
    :ivar templates: list of strings.
        List of the conjugation patterns.
    """

    def _load_cache(self, file):
        file_path = os.path.abspath(file)
        if not file_path.endswith('.xml'):
            raise ValueError(f"Invalid file path, expected .xml file, got {file_path}")
        pkl_file = file_path + '.pkl'
        
        if os.path.isfile(pkl_file):
            last_modified_time_file = os.path.getmtime(file_path)
            last_modified_time_pkl = os.path.getmtime(pkl_file)
            if last_modified_time_file <= last_modified_time_pkl:
                file_dic = joblib.load(pkl_file)
                return file_dic
        else:
            return None
    
    def _load_verbs(self, verbs_file):
        """
        Load and parses the verbs from the xml file.

        :param verbs_file: string or path object.
            Path to the verbs xml file.

        """
        self.verbs = self._parse_verbs(verbs_file.replace('json', 'xml'))
        return

    def _parse_verbs(self, file):
        """
        Parses the XML file.
    
        :param file: FileObject.
            XML file containing the verbs.
        :return verb_templates: OrderedDict.
            An OrderedDict containing the verb and its template for all verbs in the file.
    
        """
        cache = self._load_cache(file)
        if cache:
            return cache
        
        verbs_dic = {}
        xml = ET.parse(file)
        for verb in xml.findall("v"):
            verb_name = verb.find("i").text
            template = verb.find("t").text
            index = - len(template[template.index(":") + 1:])
            root = verb_name if index == 0 else verb_name[:index]
            verbs_dic[verb_name] = {"template": template, "root": root}
        
        pkl_file = file + '.pkl'
        joblib.dump(verbs_dic, pkl_file, compress = ('gzip', 3))
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
        :return conjugations: OrderedDict.
            An OrderedDict containing all the conjugation templates in the file.

        """
        cache = self._load_cache(file)
        if cache:
            return cache
                
        conjugations_dic = {}
        xml = ET.parse(file)
        for template in xml.findall("template"):
            template_name = template.get("name")
            conjugations_dic[template_name] = OrderedDict()
            for mood in list(template):
                conjugations_dic[template_name][mood.tag] = OrderedDict()
                for tense in list(mood):
                    conjugations_dic[template_name][mood.tag][tense.tag.replace('-', ' ')] = self._load_tense(tense)
        pkl_file = file + '.pkl'
        joblib.dump(conjugations_dic, pkl_file, compress = ('gzip', 3))
        return conjugations_dic

    @staticmethod
    def _load_tense(tense):
        """
        Load and parses the inflected forms of the tense from xml file.

        :param tense: list of xml tags containing inflected forms.
            The list of inflected forms for the current tense being processed.
        :return inflected_forms: list.
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
