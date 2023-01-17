#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `mlconjug3` package."""

import pytest

def test_mlconjug():
    """
    Test the functionality of the Conjugator class in the mlconjug module.
    """
    # Test the default behavior
    conjugator = Conjugator()
    assert conjugator.language == 'fr'
    assert isinstance(conjugator.conjug_manager, Verbiste)
    assert isinstance(conjugator.model, Pipeline)
    # Test the behavior when a language is provided
    conjugator = Conjugator(language='en')
    assert conjugator.language == 'en'
    assert isinstance(conjugator.conjug_manager, Verbiste)
    assert isinstance(conjugator.model, Pipeline)
    
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
    assert isinstance(conjugations, dict)
    assert set(conjugations.keys()) == set(_TENSES.keys)
    
