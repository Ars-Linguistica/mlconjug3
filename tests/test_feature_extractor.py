import pytest
import numpy as np
from feature_extractor import VerbFeatures

@pytest.fixture(scope="module")
def feature_extractor():
    return VerbFeatures()

def test_transform(feature_extractor):
    verbs = ["parler", "manger", "dormir"]
    features = feature_extractor.transform(verbs)
    assert isinstance(features, np.ndarray)
    assert features.shape[0] == len(verbs)

def test_fit(feature_extractor):
    verbs = ["parler", "manger", "dormir"]
    feature_extractor.fit(verbs)
    assert feature_extractor.char_ngrams is None
    assert feature_extractor.w2v_model is None
    assert feature_extractor.morph_features is None

def test_extract_verb_features(feature_extractor):
    verb_features = feature_extractor.extract_verb_features("parler", 'fr', (2,7))
    assert isinstance(verb_features, list)
    assert len(verb_features) > 0

