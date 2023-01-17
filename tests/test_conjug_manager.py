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

from conjug_manager import ConjugManager

@pytest.fixture(scope="module")
def conjug_manager():
    return ConjugManager()

def test_load_verbs(conjug_manager):
    assert isinstance(conjug_manager.verbs, dict)
    assert len(conjug_manager.verbs) > 0

def test_load_conjugations(conjug_manager):
    assert isinstance(conjug_manager.conjugations, dict)
    assert len(conjug_manager.conjugations) > 0

def test_get_conjug(conjug
