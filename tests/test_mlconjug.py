#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `mlconjug3` package."""

import pytest
import sys
import tempfile
import os
import yaml
import tomlkit

from sklearn.exceptions import ConvergenceWarning
import warnings

import json

from functools import partial

from click.testing import CliRunner

from collections import OrderedDict

from mlconjug3 import Conjugator, DataSet, Model, extract_verb_features, \
    LinearSVC, SGDClassifier, SelectFromModel, CountVectorizer

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
        assert self.verbiste.templates[-1] == 'écri:re'
        assert isinstance(self.verbiste.conjugations[':aller'], OrderedDict)
        assert len(self.verbiste.verbs) == 7015
        assert self.verbiste.verbs['abaisser'] == {'template': 'aim:er', 'root': 'abaiss'}

    def test_repr(self):
        assert self.verbiste.__repr__() == 'mlconjug3.conjug_manager.conjug_manager.Verbiste(language=fr)'

    def test_unsupported_language(self):
        with pytest.raises(ValueError) as excinfo:
            Verbiste(language='de')
        # assert 'Unsupported language.' in str(excinfo.value)

    def test_get_verb_info(self):
        verb_info = self.verbiste.get_verb_info('aller')
        assert verb_info == VerbInfo('aller', '', ':aller')
        assert self.verbiste.get_verb_info('cacater') is None
        assert verb_info.__repr__() == 'mlconjug3.verbs.verbs.VerbInfo(aller, , :aller)'

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
        assert test_verb.__repr__() == 'mlconjug3.verbs.verbs.VerbFr(manger)'

    def test_iterate(self):
        verbiste = Verbiste(language='default')
        test_verb_info = verbiste.get_verb_info(TEST_VERBS[verbiste.language][0])
        test_conjug_info = verbiste.get_conjug_info(TEST_VERBS[verbiste.language][1])
        test_verb = Verb(test_verb_info, test_conjug_info)
        iteration_results = test_verb.iterate()
        assert len(iteration_results) == 46
        # assert iteration_results[0] == ('Infinitif', 'Infinitif Présent', 'manger')
        assert iteration_results[1] == ('Indicatif', 'Présent', '1s', 'mange')
        
    def test_set_get_contains(self):
        verbiste = Verbiste(language='fr')
        test_verb_info = verbiste.get_verb_info(TEST_VERBS[verbiste.language][0])
        test_conjug_info = verbiste.get_conjug_info(TEST_VERBS[verbiste.language][1])
        test_verb = VerbFr(test_verb_info, test_conjug_info)
        # Test setitem with tuple
        test_verb["Indicatif", "Présent", "2s"] = "manges"
        assert test_verb.conjug_info["Indicatif"]["Présent"]["2s"] == "manges"
        # Test nested setitem
        test_verb["Indicatif"]["Présent"]["2s"] = "manges"
        assert test_verb.conjug_info["Indicatif"]["Présent"]["2s"] == "manges"
        # Test nested getitem
        assert test_verb["Indicatif"]["Présent"]["2s"] == "manges"
        # Test getitem with tuple
        assert test_verb["Indicatif", "Présent", "2s"] == "manges"
        # Test contains using string
        assert "tu manges" in test_verb
        assert "manges" in test_verb
        assert "tu parles" not in test_verb


class TestEndingCountVectorizer:
    ngrange = (2, 7)
    custom_vectorizer = partial(extract_verb_features, lang='fr', ngram_range=ngrange)
    vectorizer = CountVectorizer(analyzer=custom_vectorizer, binary=True, ngram_range=ngrange)

    def test_char_ngrams(self):
        ngrams = self.vectorizer._char_ngrams('aller')
        assert 'ller' in ngrams


class TestConjugator:
    conjugator = Conjugator()

    def test_repr(self):
        assert self.conjugator.__repr__() == 'mlconjug3.mlconjug.Conjugator(language=fr)'

    def test_conjugate(self):
        test_verb = self.conjugator.conjugate('aller')
        assert isinstance(test_verb, Verb)
        assert test_verb.verb_info == VerbInfo('aller', '', ':aller')
        test_verb = self.conjugator.conjugate('cacater')
        assert isinstance(test_verb, Verb)
        error_verb = self.conjugator.conjugate('blablah')
        assert error_verb is None

    def test_set_model(self):
        self.conjugator.set_model(Model())
        assert isinstance(self.conjugator.model, Model)


class TestDataSet:
    conjug_manager = ConjugManager()
    data_set = DataSet(conjug_manager.verbs)

    def test_repr(self):
        assert self.data_set.__repr__() == 'mlconjug3.dataset.dataset.DataSet()'

    def test_construct_dict_conjug(self):
        self.data_set.construct_dict_conjug()
        assert 'aller' in self.data_set.dict_conjug[':aller']

    def test_split_data(self):
        self.data_set.split_data()
        assert self.data_set.test_input is not None
        assert self.data_set.train_input is not None
        assert self.data_set.test_labels is not None
        assert self.data_set.train_labels is not None
        with pytest.raises(ValueError) as excinfo:
            self.data_set.split_data(proportion=2)
        # assert 'The split proportion must be between 0 and 1' in str(excinfo.value)


class TestModel:
    extract_verb_features = extract_verb_features
    vectorizer = CountVectorizer(analyzer=partial(extract_verb_features, lang='fr', ngram_range=(2, 7)), binary=True,
                                 ngram_range=(2, 7), lowercase=False)
    # Feature reduction
    feature_reductor = SelectFromModel(
        LinearSVC(penalty="l1", max_iter=3000, dual=False, verbose=2))
    # Prediction Classifier
    classifier = SGDClassifier(loss="log_loss", penalty='elasticnet', alpha=1e-5, random_state=42)
    # Initialize Model
    model = Model(vectorizer, feature_reductor, classifier)
    dataset = DataSet(Verbiste().verbs)
    dataset.construct_dict_conjug()
    dataset.split_data(proportion=0.9)

    def test_repr(self):
        assert self.model.__repr__() == 'mlconjug3.models.models.Model(classifier, feature_selector, vectorizer)'

    def test_train(self):
        self.model.train(self.dataset.test_input, self.dataset.test_labels)
        assert isinstance(self.model, Model)

    def test_predict(self):
        result = self.model.predict(['aimer', ])
        assert self.dataset.templates[result[0]] == 'aim:er'


class TestCLI:
    verbiste = Verbiste(language='fr')
    conjugator = Conjugator()

    def test_command_line_interface(self):
        """Test the CLI."""
        verb = 'aller'
        runner = CliRunner()
        result = runner.invoke(cli.main, [verb])
        assert result.exit_code == 0
        
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        # assert 'Console script for mlconjug3.' in help_result.output

    @pytest.mark.skipif('3.5' in sys.version,
                        reason="Random TypeError('invalid file') on Python 3.5.")
    def test_save_file(self, tmpdir):
        """
        Tests file saving feature.

        """
        test_verb = self.conjugator.conjugate('aller')
        path = tmpdir.mkdir("sub").join('conjugations.json')
        verb = 'aller'
        runner = CliRunner()
        result = runner.invoke(cli.main, [verb, '-o', path])
        assert result.exit_code == 0
        my_file = Path(path)
        assert my_file.is_file()
        with open(my_file, encoding='utf-8') as file:
            output = json.load(file)
        assert output['aller'] == test_verb.conjug_info
        
    def test_load_toml(self, tmpdir):
        """
        Test loading config from toml file
        """
        # Create a temporary directory
        temp_dir = tempfile.TemporaryDirectory()
        # Create a config.toml file in the temporary directory
        config_path = os.path.join(temp_dir.name, 'config.toml')
        with open(config_path, 'w') as f:
            f.write("""
            language = "en"
            subject = "abbrev"
            output = "conjugation_table.json"
            file_format = "json"
    
            [theme]
            header_style = "bold #0D47A1"
            mood_style = "bold #F9A825"
            tense_style = "bold bright_magenta"
            person_style = "bold cyan"
            conjugation_style = "bold #4CAF50"
            """)
        verb = 'aller'
        runner = CliRunner()
        result = runner.invoke(cli.main, [verb, '-c', config_path])
        assert result.exit_code == 0
        # assert 'Loading config from {}'.format(config_path) in result.output.strip()
        # add additional asserts to check that the loaded config is used in the conjugation
        temp_dir.cleanup() 
    
    def test_load_yaml(self, tmpdir):
        """
        Test loading config from toml file
        """
        # Create a temporary directory
        temp_dir = tempfile.TemporaryDirectory()
        # Create a config.yaml file in the temporary directory
        config_path = os.path.join(temp_dir.name, 'config.yaml')
        with open(config_path, 'w') as config_file:
            config = {
                'language': 'fr',
                'subject': 'pronoun',
                'output': 'conjugation_table.json',
                'file_format': 'json',
                'theme': {
                    'header_style': 'bold blue',
                    'mood_style': 'bold yellow',
                    'tense_style': 'bold green',
                    'person_style': 'bold bright_cyan',
                    'conjugation_style': 'bold bright_magenta',
                }
            }
            yaml.dump(config, config_file)
        
        # Try to load the config.yaml file from the cli
        runner = CliRunner()
        result = runner.invoke(cli.main, ['aller', '-c', config_path])
        assert result.exit_code == 0
        # assert 'Loading config from {}'.format(config_path) in result.output.strip()
        # Cleans temp dir
        temp_dir.cleanup() 


class TestConjugatorTrainer:
    @pytest.fixture(scope="class")
    def trainer(self):
        lang = "fr"
        params = {'lang': lang,
                  'output_folder': "models",
                  'split_proportion': 0.8,
                  'dataset': mlconjug3.DataSet(mlconjug3.Verbiste(lang).verbs),
                  'model': mlconjug3.Model(
                      language=lang,
                      vectorizer=mlconjug3.CountVectorizer(analyzer=partial(extract_verb_features, lang=lang, ngram_range=(2, 7)),
                                             binary=True, lowercase=False),
                      feature_selector=mlconjug3.SelectFromModel(mlconjug3.LinearSVC(penalty = "l1", max_iter = 12000, dual = False, verbose = 0)),
                      classifier=mlconjug3.SGDClassifier(loss = "log", penalty = "elasticnet", l1_ratio = 0.15, max_iter = 40000, alpha = 1e-5, verbose = 0)
                  )
                 }
        return ConjugatorTrainer(**params)
    
    def test_train(self, trainer):
        trainer.train()
        # assert trainer.is_trained == True
    
    def test_predict(self, trainer):
        trainer.predict()
        # assert trainer.predictions is not None
    
    def test_evaluate(self, trainer):
        trainer.evaluate()
        # assert trainer.evaluation is not None
    
    # def test_save(self, trainer):
        # trainer.save()
        # assert trainer.output_folder is not None

