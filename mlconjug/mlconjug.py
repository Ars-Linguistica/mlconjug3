# -*- coding: utf-8 -*-

"""
MLConjug Main module.

| This module declares the main classes the user interacts with.

| The module defines the classes needed to interface with Machine Learning models.

"""

# from mlconjug import _RESOURCE_PACKAGE, _LANGUAGE_FULL
from .PyVerbiste import Verbiste, VerbInfo, Verb, VerbEn, VerbEs, VerbFr, VerbIt, VerbPt, VerbRo

from sklearn.feature_selection import SelectFromModel
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import LinearSVC
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline

import random
from collections import defaultdict
import pickle
import pkg_resources
import re


_RESOURCE_PACKAGE = __name__

_LANGUAGE_FULL = {'fr': 'Français',
                  'en': 'English',
                  'es': 'Español',
                  'it': 'Italiano',
                  'pt': 'Português',
                  'ro': 'Română',
                  }

_VERBS = {'fr': VerbFr,
          'en': VerbEn,
          'es': VerbEs,
          'it': VerbIt,
          'pt': VerbPt,
          'ro': VerbRo,
          }

_PRE_TRAINED_MODEL_PATH = {'fr': '/'.join(('data', 'models', 'trained_model-fr-final.pickle')),
                           'it': '/'.join(('data', 'models', 'trained_model-it-final.pickle')),
                           'es': '/'.join(('data', 'models', 'trained_model-es-final.pickle')),
                           'en': '/'.join(('data', 'models', 'trained_model-en-final.pickle')),
                           'pt': '/'.join(('data', 'models', 'trained_model-pt-final.pickle')),
                           'ro': '/'.join(('data', 'models', 'trained_model-ro-final.pickle')),
                           }

_ALPHABET = {'fr': {'vowels':'aáàâeêéèiîïoôöœuûùy',
                    'consonnants': 'bcçdfghjklmnpqrstvwxyz'},
             'en': {'vowels':'aeiouy',
                    'consonnants': 'bcdfghjklmnpqrstvwxyz'},
             'es': {'vowels':'aáeiíoóuúy',
                    'consonnants': 'bcdfghjklmnñpqrstvwxyz'},
             'it': {'vowels':'aàeéèiìîoóòuùy',
                    'consonnants': 'bcdfghjklmnpqrstvwxyz'},
             'pt': {'vowels':'aàãááeêéiíoóõuúy',
                    'consonnants': 'bcçdfghjklmnpqrstvwxyz'},
             'ro': {'vowels':'aăâeiîouy',
                    'consonnants': 'bcdfghjklmnpqrsșştțţvwxyz'},
            }


def extract_verb_features(verb, lang, ngram_range):
    """
    | Custom Vectorizer optimized for extracting verbs features.
    | The Vectorizer subclasses sklearn.feature_extraction.text.CountVectorizer .
    | As in Indo-European languages verbs are inflected by adding a morphological suffix,
    the vectorizer extracts verb endings and produces a vector representation of the verb with binary features.

    | The features are the verb ending n-grams, starting n-grams, length of verb, number of vowels,
    | number of consonants and the ratio of vowels over consonants.

    :param verb: string.
        Verb to vectorize.
    :param lang: string.
        Language to analyze.
    :param ngram_range: tuple.
        The range of the ngram sliding window.
    :return: list.
        List of the most salient features of the verb for the task of finding it's conjugation's class.

    """
    _white_spaces = re.compile(r"\s\s+")
    verb = _white_spaces.sub(" ", verb)
    verb = verb.lower()
    verb_len = len(verb)
    length_feature = 'LEN={0}'.format(str(verb_len))
    min_n, max_n = ngram_range
    final_ngrams = ['END={0}'.format(verb[-n:]) for n in range(min_n, min(max_n + 1, verb_len + 1))]
    initial_ngrams = ['START={0}'.format(verb[:n]) for n in range(min_n, min(max_n + 1, verb_len + 1))]
    vowels = sum(verb.count(c) for c in _ALPHABET[lang]['vowels'])
    vowels_number = 'VOW_NUM={0}'.format(vowels)
    consonants = sum(verb.count(c) for c in _ALPHABET[lang]['consonants'])
    consonants_number = 'CONS_NUM={0}'.format(consonants)
    if consonants == 0:
        vow_cons_ratio = 'V/C=N/A'
    else:
        vow_cons_ratio = 'V/C={0}'.format(round(vowels / consonants, 2))
    final_ngrams.extend(initial_ngrams)
    final_ngrams.extend((length_feature, vowels_number, consonants_number, vow_cons_ratio))
    return final_ngrams


class Conjugator:
    """
    | This is the main class of the project.
    | The class manages the Verbiste data set and provides an interface with the scikit-learn pipeline.
    | If no parameters are provided, the default language is set to french and the pre-trained french conjugation pipeline is used.
    | The class defines the method conjugate(verb, language) which is the main method of the module.

    :param language: string.
        Language of the conjugator. The default language is 'fr' for french.
    :param model: string.
        A user provided pipeline if the user has trained his own pipeline.

    """
    def __init__(self, language='fr', model=None):
        self.language = language
        # self.verbiste = Verbiste(language=language)
        self.data_set = DataSet(Verbiste(language=language))
        self.data_set.split_data(proportion=0.9)
        if not model:
            model = pickle.loads(pkg_resources.resource_stream(
                _RESOURCE_PACKAGE, _PRE_TRAINED_MODEL_PATH[language]).read())
        self.model = model
        return

    def __repr__(self):
        return '{0}.{1}(language={2})'.format(__name__, self.__class__.__name__, self.language)

    def conjugate(self, verb, subject='abbrev'):
        """
        | This is the main method of this class.
        | It first checks to see if the verb is in Verbiste.
        | If it is not, and a pre-trained scikit-learn pipeline has been supplied, the method then calls the pipeline
        to predict the conjugation class of the provided verb.

        | Returns a Verb object or None.

        :param verb: string.
            Verb to conjugate.
        :param subject: string.
            Toggles abbreviated or full pronouns.
            The default value is 'abbrev'.
            Select 'pronoun' for full pronouns.
        :return: Verb object or None.

        """
        prediction_score = 0
        predicted = False
        if not self.data_set.verbiste.is_valid_verb(verb):
            raise ValueError(_('The supplied word: {0} is not a valid verb in {1}.').format(verb, _LANGUAGE_FULL[self.language]))
        if verb not in self.data_set.verbiste.verbs.keys():
            if self.model is None:
                return None
            prediction = self.model.predict([verb])[0]
            prediction_score = self.model.pipeline.predict_proba([verb])[0][prediction]
            predicted = True
            template = self.data_set.verbiste.templates[prediction]
            index = - len(template[template.index(":") + 1:])
            root = verb[:index]
            verb_info = VerbInfo(verb, root, template)
            conjug_info = self.data_set.verbiste.get_conjug_info(verb_info.template)
        else:
            predicted = False
            infinitive = verb
            verb_info = self.data_set.verbiste.get_verb_info(infinitive)
            if verb_info is None:
                return None
            conjug_info = self.data_set.verbiste.get_conjug_info(verb_info.template)
            if conjug_info is None:
                return None
        if predicted:
            verb_object = _VERBS[self.language](verb_info, conjug_info, subject, predicted)
            verb_object.predicted = predicted
            verb_object.prediction_score = round(prediction_score, 3)
        else:
            verb_object = _VERBS[self.language](verb_info, conjug_info, subject)

        return verb_object

    def set_model(self, model):
        """
        Assigns the provided pre-trained scikit-learn pipeline to be able to conjugate unknown verbs.

        :param model: scikit-learn Classifier or Pipeline.

        """
        assert isinstance(model, Model), _('Please provide an instance of a mlconjug.mlconjug.Model')
        self.model = model
        return


class DataSet:
    """
    | This class holds and manages the data set.
    | Defines helper functions for managing Machine Learning tasks like constructing a training and testing set.

    :param VerbisteObj:
        Instance of a Verbiste object.

    """
    def __init__(self, VerbisteObj):
        self.verbiste = VerbisteObj
        self.verbs = self.verbiste.verbs.keys()
        self.templates = sorted(self.verbiste.conjugations.keys())
        self.verbs_list = []
        self.templates_list = []
        self.dict_conjug = {}
        self.train_input = []
        self.train_labels = []
        self.test_input = []
        self.test_labels = []
        self.construct_dict_conjug()
        return

    def __repr__(self):
        return '{0}.{1}({2})'.format(__name__, self.__class__.__name__, self.verbiste.__repr__)

    def construct_dict_conjug(self):
        """
        | Populates the dictionary containing the conjugation templates.
        | Populates the lists containing the verbs and their templates.

        """
        conjug = defaultdict(list)
        for verbe, info_verbe in self.verbiste.verbs.items():
            self.verbs_list.append(verbe)
            self.templates_list.append(self.templates.index(info_verbe["template"]))
            conjug[info_verbe["template"]].append(verbe)
        self.dict_conjug = conjug
        return

    def split_data(self, threshold=8, proportion=0.5):
        """
        Splits the data into a training and a testing set.

        :param threshold: int.
            Minimum size of conjugation class to be split.
        :param proportion: float.
            Proportion of samples in the training set.
            Must be between 0 and 1.

        """
        if proportion <= 0 or proportion >= 1:
            raise ValueError(_('The split proportion must be between 0 and 1.'))
        self.min_threshold = threshold
        self.split_proportion = proportion
        train_set = []
        test_set = []
        for template, lverbs in self.dict_conjug.items():
            if len(lverbs) <= threshold:
                for verbe in lverbs:
                    train_set.append((verbe, template))
            else:
                index = round(len(lverbs) * proportion)
                for verbe in lverbs[:index]:
                    train_set.append((verbe, template))
                for verbe in lverbs[index:]:
                    test_set.append((verbe, template))
        random.shuffle(train_set)
        random.shuffle(test_set)
        self.train_input = [elmt[0] for elmt in train_set]
        self.train_labels = [self.templates.index(elmt[1]) for elmt in train_set]
        self.test_input = [elmt[0] for elmt in test_set]
        self.test_labels = [self.templates.index(elmt[1]) for elmt in test_set]
        return


class Model(object):
    """
    | This class manages the scikit-learn pipeline.
    | The Pipeline includes a feature vectorizer, a feature selector and a classifier.
    | If any of the vectorizer, feature selector or classifier is not supplied at instance declaration,
    the __init__ method will provide good default values that get more than 92% prediction accuracy.

    :param vectorizer: scikit-learn Vectorizer.
    :param feature_selector: scikit-learn Classifier with a fit_transform() method
    :param classifier: scikit-learn Classifier with a predict() method

    """
    def __init__(self, vectorizer=None, feature_selector=None, classifier=None):
        if not vectorizer:
            vectorizer = CountVectorizer(analyzer=extract_verb_features, binary=True, ngram_range=(2, 7))
        if not feature_selector:
            feature_selector = SelectFromModel(LinearSVC(penalty='l1', max_iter=12000, dual=False, verbose=2))
        if not classifier:
            classifier = SGDClassifier(loss='log', penalty='elasticnet', l1_ratio=0.15,
                                       max_iter=4000, alpha=1e-5, random_state=42, verbose=2)
        self.pipeline = Pipeline([('vectorizer', vectorizer),
                                  ('feature_selector', feature_selector),
                                  ('classifier', classifier)])
        return

    def __repr__(self):
        return '{0}.{1}({2}, {3}, {4})'.format(__name__, self.__class__.__name__, *sorted(self.pipeline.named_steps))

    def train(self, samples, labels):
        """
        Trains the pipeline on the supplied samples and labels.

        :param samples: list.
            List of verbs.
        :param labels: list.
            List of verb templates.

        """
        self.pipeline = self.pipeline.fit(samples, labels)
        return

    def predict(self, verbs):
        """
        Predicts the conjugation class of the provided list of verbs.

        :param verbs: list.
            List of verbs.
        :return: list.
            List of predicted conjugation groups.

        """
        prediction = self.pipeline.predict(verbs)
        return prediction


if __name__ == "__main__":
    pass
