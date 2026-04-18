#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `mlconjug3` package."""

import pytest
import sys
import tempfile
import os
import yaml
import numpy as np

from sklearn.exceptions import ConvergenceWarning
import warnings
import json

from functools import partial

from click.testing import CliRunner

from collections import OrderedDict

from mlconjug3 import Conjugator, DataSet, Model, extract_verb_features, \
    SGDClassifier, CountVectorizer

from mlconjug3 import Verbiste, VerbInfo, Verb, VerbEn, \
    VerbEs, VerbFr, VerbIt, VerbPt, VerbRo, ConjugManager

from mlconjug3 import cli
from mlconjug3.utils import ConjugatorTrainer

import mlconjug3

try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=ConvergenceWarning)


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


class TestPyVerbiste:
    verbiste = Verbiste(language='fr')
    verbiste_en = Verbiste(language='en')

    def test_init_verbiste(self):
        assert len(self.verbiste.templates) == len(self.verbiste.conjugations) == 149
        assert self.verbiste.templates[0] == ':aller'
        assert isinstance(self.verbiste.conjugations[':aller'], OrderedDict)

    def test_repr(self):
        assert self.verbiste.__repr__() == 'mlconjug3.conjug_manager.conjug_manager.Verbiste(language=fr)'

    def test_get_verb_info(self):
        verb_info = self.verbiste.get_verb_info('aller')
        assert verb_info == VerbInfo('aller', '', ':aller')
        assert self.verbiste.get_verb_info('cacater') is None

    def test_get_conjug_info(self):
        conjug_info = self.verbiste.get_conjug_info(':aller')
        assert conjug_info == self.verbiste.conjugations[':aller']

    def test_is_valid_verb(self):
        assert self.verbiste.is_valid_verb('manger')
        assert not self.verbiste.is_valid_verb('banane')


class TestVerb:
    @pytest.mark.parametrize('lang', LANGUAGES)
    def test_verbinfo(self, lang):
        verbiste = Verbiste(language=lang)
        test_verb_info = verbiste.get_verb_info(TEST_VERBS[verbiste.language][0])
        test_conjug_info = verbiste.get_conjug_info(TEST_VERBS[verbiste.language][1])
        test_verb = VERBS[verbiste.language](test_verb_info, test_conjug_info)
        assert isinstance(test_verb, VERBS[verbiste.language])

    def test_repr(self):
        verbiste = Verbiste(language='fr')
        test_verb_info = verbiste.get_verb_info('manger')
        test_conjug_info = verbiste.get_conjug_info('man:ger')
        test_verb = VerbFr(test_verb_info, test_conjug_info)
        assert test_verb.__repr__() == 'mlconjug3.verbs.verbs.VerbFr(manger)'


class TestConjugator:
    conjugator = Conjugator()

    def test_repr(self):
        assert self.conjugator.__repr__() == 'mlconjug3.mlconjug.Conjugator(language=fr)'

    def test_conjugate(self):
        test_verb = self.conjugator.conjugate('aller')
        assert isinstance(test_verb, Verb)

        # ML fallback now ALWAYS returns a Verb
        test_verb = self.conjugator.conjugate('cacater')
        assert isinstance(test_verb, Verb)

        test_verb = self.conjugator.conjugate('blablah')
        assert isinstance(test_verb, Verb)


class TestDataSet:
    conjug_manager = ConjugManager()
    data_set = DataSet(conjug_manager.verbs)

    def test_split_data(self):
        self.data_set.split_data()
        assert self.data_set.train_input is not None


class TestModel:
    model = Model(language='fr')

    dataset = DataSet(Verbiste().verbs)
    dataset.construct_dict_conjug()
    dataset.split_data(proportion=0.9)

    def test_repr(self):
        assert isinstance(self.model.__repr__(), str)

    def test_train(self):
        self.model.train(self.dataset.train_input, self.dataset.train_labels)
        assert isinstance(self.model, Model)

    def test_predict(self):
        result = self.model.predict(['aimer'])
        assert isinstance(result[0], (int, np.integer))


class TestCLI:
    conjugator = Conjugator()

    def test_command_line_interface(self):
        runner = CliRunner()
        result = runner.invoke(cli.main, ['aller'])
        assert result.exit_code == 0


class TestConjugatorTrainer:
    @pytest.fixture(scope="class")
    def trainer(self):
        lang = "fr"
        return ConjugatorTrainer(
            lang=lang,
            output_folder="models",
            split_proportion=0.8,
            dataset=mlconjug3.DataSet(mlconjug3.Verbiste(lang).verbs),
            model=mlconjug3.Model(language=lang),
        )

    def test_train(self, trainer):
        trainer.train()

    def test_predict(self, trainer):
        trainer.predict()

    def test_evaluate(self, trainer):
        trainer.evaluate()
