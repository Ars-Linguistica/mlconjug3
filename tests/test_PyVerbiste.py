import os
import json
import defusedxml.ElementTree as ET
import pytest
from mlconjug3 import *

# fixture to load the verbiste data
@pytest.fixture
def verbiste():
    with open(os.path.join('path', 'to', 'verbiste_data.json')) as f:
        verbiste_data = json.load(f)
    return verbiste_data

def test_parse_verbs(verbiste):
    # test that the parse verbs function correctly parses the xml data
    xml_file = os.path.join('path', 'to', 'verbiste_verbs.xml')
    verbs = Verbiste._parse_verbs(xml_file)
    assert verbs == verbiste['verbs']

def test_parse_conjugations(verbiste):
    # test that the parse conjugations function correctly parses the xml data
    xml_file = os.path.join('path', 'to', 'verbiste_conjugations.xml')
    conjugations = Verbiste._parse_conjugations(xml_file)
    assert conjugations == verbiste['conjugations']

def test_load_verbs(verbiste, monkeypatch):
    pass
    # test that the load verbs function correctly loads the verbs from the file
    # TODO
    # def mock_parse_verbs
