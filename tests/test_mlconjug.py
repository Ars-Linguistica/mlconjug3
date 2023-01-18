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
    conjug_manager = ConjugManager()
    data_set = DataSet(conjug_manager.verbs)

    def test_repr(self):
        assert self.data_set.__repr__() == 'mlconjug3.mlconjug.DataSet'

        
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

    def test_repr(self):
        assert self.model.__repr__() == 'mlconjug3.mlconjug.Model'


