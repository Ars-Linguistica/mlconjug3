#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `mlconjug3` package."""

import pytest
from mlconjug3 import *
from sklearn.exceptions import ConvergenceWarning
import warnings

try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=ConvergenceWarning)

class TestEndingCountVectorizer:
    ngrange = (2, 7)
    custom_vectorizer = partial(extract_verb_features, lang='fr', ngram_range=ngrange)
    vectorizer = CountVectorizer(analyzer=custom_vectorizer, binary=True, ngram_range=ngrange)

    def test_char_ngrams(self):
        ngrams = self.vectorizer._char_ngrams('aller')
        assert 'ller' in ngrams


class TestConjugator:
    conjugator = Conjugator()

    def test_repr(self):
        assert self.conjugator.__repr__() == 'mlconjug3.mlconjug.Conjugator(language=fr)'

    def test_conjugate(self):
        test_verb = self.conjugator.conjugate('aller')
        assert isinstance(test_verb, Verb)
        assert test_verb.verb_info == VerbInfo('aller', '', ':aller')
        test_verb = self.conjugator.conjugate('cacater')
        assert isinstance(test_verb, Verb)
        with pytest.raises(ValueError) as excinfo:
            self.conjugator.conjugate('blablah')
            assert 'The supplied word: blablah is not a valid verb in French.' in str(excinfo.value)

    def test_set_model(self):
        self.conjugator.set_model(Model())
        assert isinstance(self.conjugator.model, Model)


class TestDataSet:
    conjug_manager = ConjugManager()
    data_set = DataSet(conjug_manager.verbs)

    def test_repr(self):
        assert self.data_set.__repr__() == 'mlconjug3.mlconjug.DataSet()'

    def test_construct_dict_conjug(self):
        self.data_set.construct_dict_conjug()
        assert 'aller' in self.data_set.dict_conjug[':aller']

    def test_split_data(self):
        self.data_set.split_data()
        assert self.data_set.test_input is not None
        assert self.data_set.train_input is not None
        assert self.data_set.test_labels is not None
        assert self.data_set.train_labels is not None
        with pytest.raises(ValueError) as excinfo:
            self.data_set.split_data(proportion=2)
        # assert 'The split proportion must be between 0 and 1' in str(excinfo.value)


class TestModel:
    extract_verb_features = extract_verb_features
    vectorizer = CountVectorizer(analyzer=partial(extract_verb_features, lang='fr', ngram_range=(2, 7)), binary=True,
                                 ngram_range=(2, 7), lowercase=False)
    # Feature reduction
    feature_reductor = SelectFromModel(
        LinearSVC(penalty="l1", max_iter=3000, dual=False, verbose=2))
    # Prediction Classifier
    classifier = SGDClassifier(loss="log", penalty='elasticnet', alpha=1e-5, random_state=42)
    # Initialize Model
    model = Model(vectorizer, feature_reductor, classifier)
    dataset = DataSet(Verbiste().verbs)
    dataset.construct_dict_conjug()
    dataset.split_data(proportion=0.9)

    def test_repr(self):
        assert self.model.__repr__() == 'mlconjug3.mlconjug.Model(classifier, feature_selector, vectorizer)'

    def test_train(self):
        self.model.train(self.dataset.test_input, self.dataset.test_labels)
        assert isinstance(self.model, Model)

    def test_predict(self):
        result = self.model.predict(['aimer', ])
        assert self.dataset.templates[result[0]] == 'aim:er'