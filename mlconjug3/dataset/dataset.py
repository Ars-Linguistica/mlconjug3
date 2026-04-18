"""
Dataset management module for mlconjug3.

This module defines the DataSet class, which is responsible for organizing
verb data and preparing it for machine learning tasks such as training
and evaluation.

It supports dataset shuffling, template indexing, and splitting into
training and testing subsets.
"""

from random import Random
from collections import defaultdict
from mlconjug3.constants import *


class DataSet:
    """
    Container for verb datasets used in machine learning conjugation tasks.

    This class organizes verbs by their conjugation templates, shuffles
    the dataset, and prepares training and testing splits.

    Parameters
    ----------
    verbs_dict : dict
        Dictionary mapping verbs to their metadata, including conjugation templates.

    Attributes
    ----------
    verbs_dict : dict
        Input dictionary of verbs and metadata.
    verbs : dict_keys
        All verb keys in the dataset.
    templates : list of str
        Sorted list of unique conjugation templates.
    verbs_list : list of str
        Shuffled list of verbs.
    templates_list : list of int
        Template index corresponding to each verb in `verbs_list`.
    dict_conjug : dict
        Mapping of templates to lists of verbs belonging to them.
    min_threshold : int
        Minimum number of verbs required to split a class into train/test.
    split_proportion : float
        Ratio used for splitting data into training and testing sets.
    train_input : list of str
        Training verbs.
    train_labels : list of int
        Template indices for training verbs.
    test_input : list of str
        Testing verbs.
    test_labels : list of int
        Template indices for testing verbs.
    """

    def __init__(self, verbs_dict):
        self.verbs_dict = verbs_dict
        self.verbs = self.verbs_dict.keys()
        self.templates = sorted({verb["template"] for verb in self.verbs_dict.values()})

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

    def __repr__(self):
        """
        String representation of the DataSet object.
        """
        return "{}.{}()".format(__name__, self.__class__.__name__)

    def construct_dict_conjug(self):
        """
        Build internal dataset structures.

        This method:
        - Groups verbs by conjugation template
        - Creates shuffled verb and label lists
        - Builds a mapping from templates to verbs
        """
        conjug = defaultdict(list)

        verb_items = list(self.verbs_dict.items())
        Random(42).shuffle(verb_items)

        for verb, info_verb in verb_items:
            self.verbs_list.append(verb)
            self.templates_list.append(
                self.templates.index(info_verb["template"])
            )
            conjug[info_verb["template"]].append(verb)

        self.dict_conjug = conjug

    def split_data(self, threshold=8, proportion=0.5):
        """
        Split dataset into training and testing sets.

        Parameters
        ----------
        threshold : int, default=8
            Minimum number of samples in a class required to perform a split.
            Smaller classes are fully assigned to the training set.

        proportion : float, default=0.5
            Fraction of samples per class used for training.
            Must be between 0 and 1.

        Raises
        ------
        ValueError
            If `proportion` is not in the interval (0, 1].

        Notes
        -----
        - Classes below the threshold are not split.
        - Random seed is fixed for reproducibility.
        """
        if proportion <= 0 or proportion > 1:
            raise ValueError(_("The split proportion must be between 0 and 1."))

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
        self.train_labels = [
            self.templates.index(elmt[1]) for elmt in train_set
        ]

        self.test_input = [elmt[0] for elmt in test_set]
        self.test_labels = [
            self.templates.index(elmt[1]) for elmt in test_set
        ]


if __name__ == "__main__":
    pass
