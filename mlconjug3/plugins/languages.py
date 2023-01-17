import json
import re
from collections import defaultdict
from functools import partial
from typing import Tuple
from joblib import Memory
import hashlib
import os
import pickle
import logging

from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline

class Conjugator():
    def __init__(self, language='fr', extract_verb_features=None, pre_trained_models=None):
        self.logger = logging.getLogger(__name__)
        self.language = language
        self.extract_verb_features = extract_verb_features
        self.pre_trained_models = pre_trained_models
        self.cache = Memory(location= './cachedir', verbose=0)

        self.language_plugins = []
        self.load_language_plugins()

    def load_language_plugins(self):
        """
        This method will search for all language plugins in the designated plugin directory and load them.
        """
        for plugin in os.listdir("plugins/languages"):
            if plugin.endswith(".py"):
                try:
                    module = importlib.import_module("plugins.languages." + plugin[:-3])
                    self.language_plugins.append(module)
                    self.logger.info("Successfully loaded language plugin: {}".format(module))
                    
                except Exception as e:
                    self.logger.error("Failed to load language plugin {}: {}".format(plugin, e))

    def conjugate(self, verb, subject):
        """
        This method takes in a verb and subject, and returns the conjugated forms of the verb.
        It first checks if the verb is in the cached conjugations, if not, it uses the pre-trained models
        and language specific plugin to find the conjugations of the verb.
        """
        conjug_info = self.cache.get(verb + subject)
        if conjug_info is None:
            # extract verb features
            verb_features = self.extract_verb_features.transform([verb])
            # select features using pre-trained feature selector
            selected_features = self.pre_trained_models['feature_selector'].transform(verb_features)
            # classify verb using pre-trained classifier
            conjug_class = self.pre_trained_models['classifier'].predict(selected
