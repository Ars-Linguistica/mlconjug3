import os
import json
import defusedxml.ElementTree as ET
import pytest
from mlconjug3 import *

class TestPyVerbiste:
    verbiste = Verbiste(language='fr')
    verbiste_en = Verbiste(language='en')

    def test_init_verbiste(self):
        assert len(self.verbiste.templates) == len(self.verbiste.conjugations) == 149
        assert self.verbiste.templates[0] == ':aller'
        assert self.verbiste.templates[-1] == 'écri:re'
        assert isinstance(self.verbiste.conjugations[':aller'], OrderedDict)
        assert len(self.verbiste.verbs) == 7015
        assert self.verbiste.verbs['abaisser'] == {'template': 'aim:er', 'root': 'abaiss'}

    def test_repr(self):
        assert self.verbiste.__repr__() == 'mlconjug3.PyVerbiste.Verbiste(language=fr)'

    def test_unsupported_language(self):
        with pytest.raises(ValueError) as excinfo:
            Verbiste(language='de')
        # assert 'Unsupported language.' in str(excinfo.value)

    def test_get_verb_info(self):
        verb_info = self.verbiste.get_verb_info('aller')
        assert verb_info == VerbInfo('aller', '', ':aller')
        assert self.verbiste.get_verb_info('cacater') is None
        assert verb_info.__repr__() == 'mlconjug3.verbs.VerbInfo(aller, , :aller)'

    def test_get_conjug_info(self):
        conjug_info = self.verbiste.get_conjug_info(':aller')
        conjug_info2 = self.verbiste.get_conjug_info('man:ger')
        assert conjug_info != conjug_info2
        assert conjug_info == self.verbiste.conjugations[':aller']
        assert self.verbiste.get_conjug_info(':cacater') is None

    def test_is_valid_verb(self):
        assert self.verbiste.is_valid_verb('manger')
        assert not self.verbiste.is_valid_verb('banane')
        assert self.verbiste_en.is_valid_verb('bring')
