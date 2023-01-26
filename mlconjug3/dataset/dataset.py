"""
This module contains the DataSet class, which holds and manages the data set for conjugating verbs.

It defines helper methods for managing Machine Learning tasks like constructing a training and testing set.
"""

from random import Random
from collections import defaultdict
from mlconjug3.constants import *

class DataSet:
    """
    | This class holds and manages the data set.
    | Defines helper methodss for managing Machine Learning tasks like constructing a training and testing set.
    
    :param verbs_dict:
        A dictionary of verbs and their corresponding conjugation class.
    :ivar verbs_dict:
        A dictionary of verbs and their corresponding conjugation class.
    :ivar verbs:
        A list of all the verbs in the data set.
    :ivar templates:
        A list of all the templates in the data set.
    :ivar verbs_list:
        A list of all the verbs in the data set, shuffled randomly.
    :ivar templates_list:
        A list of the template index of each verb in the shuffled verbs_list.
    :ivar dict_conjug:
        A dictionary where the keys are conjugation templates and the values are the verbs that belong to that template.
    :ivar min_threshold:
        The minimum number of verbs in a conjugation class for it to be split into a training and testing set.
    :ivar split_proportion:
        The proportion of the data set that should be used as the training set.
    :ivar train_input:
        A list of the verbs in the training set.
    :ivar train_labels:
        A list of the template index of each verb in the training set.
    :ivar test_input:
        A list of the verbs in the testing set.
    :ivar test_labels:
        A list of the template index of each verb in the testing set.
    """

    def __init__(self, verbs_dict):
        self.verbs_dict = verbs_dict
        self.verbs = self.verbs_dict.keys()
        self.templates = sorted(
            {verb['template'] for verb in self.verbs_dict.values()}
        )

        self.verbs_list = []
        self.templates_list = []
        self.dict_conjug = None
        self.min_threshold = 8
        self.split_proportion = 0.5
        self.train_input = []
        self.train_labels = []
        self.test_input = []
        self.test_labels = []
        self.construct_dict_conjug()
        return

    def __repr__(self):
        return '{}.{}()'.format(__name__, self.__class__.__name__)

    def construct_dict_conjug(self):
        """
        | Populates the dictionary containing the conjugation templates.
        | Populates the lists containing the verbs and their templates.
        """
        conjug = defaultdict(list)
        verb_items = list(self.verbs_dict.items())
        Random(42).shuffle(verb_items)
        for verb, info_verb in verb_items:
            self.verbs_list.append(verb)
            self.templates_list.append(self.templates.index(info_verb["template"]))
            conjug[info_verb["template"]].append(verb)
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
        :raises: ValueError.
        """
        if proportion <= 0 or proportion > 1:
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
        Random(42).shuffle(train_set)
        Random(42).shuffle(test_set)
        self.train_input = [elmt[0] for elmt in train_set]
        self.train_labels = [self.templates.index(elmt[1]) for elmt in train_set]
        self.test_input = [elmt[0] for elmt in test_set]
        self.test_labels = [self.templates.index(elmt[1]) for elmt in test_set]
        return
      
if __name__ == "__main__":
    pass
