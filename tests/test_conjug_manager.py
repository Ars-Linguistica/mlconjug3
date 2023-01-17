import json
import re
from collections import defaultdict
from functools import partial
from typing import Tuple
from joblib import Memory
import hashlib
import os
import pickle

import pytest

from mlconjug3 import *

@pytest.fixture(scope="module")
def conjug_manager():
    return ConjugManager()

def test_load_verbs(conjug_manager):
    assert isinstance(conjug_manager.verbs, dict)
    assert len(conjug_manager.verbs) > 0

def test_load_conjugations(conjug_manager):
    assert isinstance(conjug_manager.conjugations, dict)
    assert len(conjug_manager.conjugations) > 0

def test_get_conjug(conjugmanager):
# Test getting the conjugation of a verb in the present tense
verb = "parler"
conjugation = conjug_manager.get_conjug(verb, tense="present", subject="je")
assert isinstance(conjugation, str)
assert conjugation == "parle"
# Test getting the conjugation of a verb in the past tense
verb = "parler"
conjugation = conjug_manager.get_conjug(verb, tense="past", subject="je")
assert isinstance(conjugation, str)
assert conjugation == "ai parlé"

# Test getting the conjugation of a verb that doesn't exist
with pytest.raises(ValueError) as excinfo:
    conjug_manager.get_conjug("fakeverb", tense="present", subject="je")
assert str(excinfo.value) == "Verb not found in conjugation data."

def test_get_verb_root(conjug_manager):
    verb = "parler"
    root = conjug_manager.get_verb_root(verb)
    assert isinstance(root, str)
    assert root == "parl"
    
def test_get_verb_template(conjug_manager):
    verb = "parler"
    template = conjug_manager.get_verb_template(verb)
    assert isinstance(template, str)
    assert template == ":er"
    
def test_get_verb_info(conjug_manager):
    verb = "parler"
    verb_info = conjug_manager.get_verb_info(verb)
    assert isinstance(verb_info, Tuple)
    assert verb_info[0] == "parl"
    assert verb_info[1] == ":er"
    
def test_get_conjug_template(conjug_manager):
    verb = "parler"
    template = conjug_manager.get_conjug_template(verb)
    assert isinstance(template, dict)
    assert "present" in template
    assert "past" in template
    assert "participle" in template
    
def test_get_conjug_template_missing_verb(conjug_manager):
    with pytest.raises(ValueError) as excinfo:
    conjug_manager.get_conjug_template("fakeverb")
    assert str(excinfo.value) == "Verb not found in conjugation data."
    
def test_detect_allowed_endings(conjug_manager):
    assert isinstance(conjug_manager._allowed_endings, list)
    assert len(conjug_manager._allowed_endings) > 0
    assert ".er" in conjug_manager._allowed_endings
    
def test_get_infinitive(conjug_manager):
    conjugated_verb = "parle"
    infinitive = conjug_manager.get_infinitive(conjugated_verb)
    assert isinstance(infinitive, str)
    assert infinitive == "parler"
