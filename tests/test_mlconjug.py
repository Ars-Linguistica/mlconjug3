#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `mlconjug3` package."""

import pytest
from mlconjug3 import *

def test_mlconjug():
    """
    Test the functionality of the Conjugator class in the mlconjug module.
    """
    # Test the default behavior
    conjugator = Conjugator()
    assert conjugator.language == 'fr'
    assert isinstance(conjugator.conjug_manager, Verbiste)
    assert isinstance(conjugator.model, Model)
    # Test the behavior when a language is provided
    conjugator = Conjugator(language='en')
    assert conjugator.language == 'en'
    assert isinstance(conjugator.conjug_manager, Verbiste)
    assert isinstance(conjugator.model, Model)
    
    # Test the behavior when a model is provided
    model = Pipeline([('vectorizer', CountVectorizer()), ('classifier', LinearSVC())])
    conjugator = Conjugator(model=model)
    assert conjugator.language == 'fr'
    assert isinstance(conjugator.conjug_manager, Verbiste)
    assert isinstance(conjugator.model, Pipeline)
    assert conjugator.model == model
    
    # Test the conjugate method
    verb = 'manger'
    conjugations = conjugator.conjugate(verb)
    assert isinstance(conjugations, Verb)
    
class TestDataSet:
    def test_load_data(self):
        dataset = DataSet(Verbiste().verbs)
        dataset._load_data()
        assert dataset.data is not None
        assert len(dataset.data) > 0

    def test_prepare_data(self):
        dataset = DataSet(Verbiste().verbs)
        dataset._load_data()
        dataset._prepare_data()
        assert len(dataset.X) > 0
        assert len(dataset.y) > 0
        assert len(dataset.X) == len(dataset.y)
    
    def test_get_train_test_data(self):
        dataset = DataSet(Verbiste().verbs)
        dataset._load_data()
        dataset._prepare_data()
        X_train, X_test, y_train, y_test = dataset.get_train_test_data()
        assert len(X_train) > 0
        assert len(X_test) > 0
        assert len(y_train) > 0
        assert len(y_test) > 0
    
    def test_get_data(self):
        dataset = DataSet(Verbiste().verbs)
        dataset._load_data()
        dataset._prepare_data()
        X, y = dataset.get_data()
        assert len(X) > 0
        assert len(y) > 0
        assert len(X) == len(y)
    
    def test_repr(self):
        dataset = DataSet(Verbiste().verbs)
        assert 'mlconjug3.mlconjug.DataSet' in data_set.__repr__()

        
class TestModel:
    def setup(self):
        self.dataset = DataSet(Verbiste().verbs)
        self.dataset._load_data()
        self.test_verb = "parler"
        self.test_conjugator = Conjugator()
        self.test_model = Model()
        self.test_model.fit(self.dataset.X, self.dataset.y)

    def test_fit(self):
        self.test_model.fit(self.dataset.X, self.dataset.y)
        assert self.test_model.is_fitted == True
    
    def test_predict(self):
        result = self.test_model.predict(self.test_verb)
        assert result is not None
    
    def test_evaluate(self):
        score = self.test_model.evaluate(self.dataset.data)
        assert score >= 0 and score <= 1
    
    def test_save(self):
        self.test_model.save("test_model.pickle")
        assert os.path.exists("test_model.pickle")
    
    def test_load(self):
        self.test_model.save("test_model.pickle")
        loaded_model = Model()
        loaded_model.load("test_model.pickle")
        assert loaded_model.is_fitted == True
    
    def test_extract_verb_features(self):
        result = self.test_model.extract_verb_features(self.test_verb)
        assert result is not None and isinstance(result, list)
    
    def test_repr(self):
        assert 'mlconjug3.mlconjug.Model' in self.test_model.__repr__()


