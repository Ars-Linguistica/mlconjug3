import pytest

from mlconjug3 import *


LANGUAGES = ('default', 'fr', 'en', 'es', 'it', 'pt', 'ro')

VERBS = {'default': Verb,
         'fr': VerbFr,
         'en': VerbEn,
         'es': VerbEs,
         'it': VerbIt,
         'pt': VerbPt,
         'ro': VerbRo}

TEST_VERBS = {'fr': ('manger', 'man:ger'),
              'en': ('bring', 'br:ing'),
              'es': ('gallofar', 'cort:ar'),
              'it': ('lavare', 'lav:are'),
              'pt': ('anunciar', 'compr:ar'),
              'ro': ('cambra', 'dans:a')}

class TestVerb:
    @pytest.mark.parametrize('lang', LANGUAGES)
    def test_verbinfo(self, lang):
        verbiste = Verbiste(language=lang)
        test_verb_info = verbiste.get_verb_info(TEST_VERBS[verbiste.language][0])
        test_conjug_info = verbiste.get_conjug_info(TEST_VERBS[verbiste.language][1])
        test_verb = VERBS[verbiste.language](test_verb_info, test_conjug_info)
        assert isinstance(test_verb, VERBS[verbiste.language])
        assert isinstance(test_verb.conjug_info, OrderedDict)

    def test_default_verb(self):
        verbiste = Verbiste(language='default')
        test_verb_info = verbiste.get_verb_info(TEST_VERBS[verbiste.language][0])
        test_conjug_info = verbiste.get_conjug_info(TEST_VERBS[verbiste.language][1])
        test_verb = Verb(test_verb_info, test_conjug_info)
        assert isinstance(test_verb, Verb)
        assert isinstance(test_verb.conjug_info, OrderedDict)

    def test_repr(self):
        verbiste = Verbiste(language='fr')
        test_verb_info = verbiste.get_verb_info(TEST_VERBS[verbiste.language][0])
        test_conjug_info = verbiste.get_conjug_info(TEST_VERBS[verbiste.language][1])
        test_verb = VerbFr(test_verb_info, test_conjug_info)
        assert test_verb.__repr__() == 'mlconjug3.PyVerbiste.VerbFr(manger)'

    def test_iterate(self):
        verbiste = Verbiste(language='default')
        test_verb_info = verbiste.get_verb_info(TEST_VERBS[verbiste.language][0])
        test_conjug_info = verbiste.get_conjug_info(TEST_VERBS[verbiste.language][1])
        test_verb = Verb(test_verb_info, test_conjug_info)
        iteration_results = test_verb.iterate()
        assert len(iteration_results) == 46
        assert iteration_results[0] == ('Infinitif', 'Infinitif Présent', 'manger')
        assert iteration_results[1] == ('Indicatif', 'Présent', '1s', 'mange')

