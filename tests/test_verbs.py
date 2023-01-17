import pytest

from verbs import VerbFr, VerbEn, VerbInfo

# Fixtures
@pytest.fixture
def verb_fr():
    verb_info = VerbInfo("manger", "mang", "er:er")
    conjug_info = {"indicatif": {"présent": {"1s": "mange", "2s": "manges", "3s": "mange", "1p": "mangeons", "2p": "mangez", "3p": "mangent"}}}
    return VerbFr(verb_info, conjug_info)

# Test functions
def test_verb_info(verb_fr, verb_en):
    assert verb_fr.verb_info.infinitive == "manger"
    assert verb_fr.verb_info.root == "mang"
