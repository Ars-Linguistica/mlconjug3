import multiprocessing
import mlconjug3
import pickle
import numpy as np
from functools import partial
from time import time

class ConjugatorTrainer:
    def __init__(self, lang, output_folder, split_proportion, feature_extractor, DataSet, Model):
        self.lang = lang
        self.output_folder = output_folder
        self.split_proportion = split_proportion
        self.feature_extractor = feature_extractor
        self.DataSet = DataSet
        self.Model = Model
        return

    def train(self):
        np.random.seed(42)

        # Initialize Data Set
        dataset = self.DataSet(
            mlconjug3.Verbiste(language=self.lang).verbs,
            feature_extractor=self.feature_extractor,
        )
        dataset.split_data(proportion=self.split_proportion)

        # Initialize Conjugator
        conjugator = mlconjug3.Conjugator(
            self.lang,
            feature_extractor=dataset.feature_extractor,
            model=self.Model,
        )

        # Train Conjugator
        result = conjugator.model.train(dataset.verbs_list, dataset.templates_list)

        # Print training duration
        print(f"{self.lang} model trained on full data set in {result} seconds.")
        return

    def predict(self, verbs_list):
        return self.conjugator.model.predict(verbs_list)

    def evaluate(self, predictions, templates_list):
        score = len(
            [a == b for a, b in zip(predictions, templates_list) if a == b]
        ) / len(predictions)
        misses = len(
            [a != b for a, b in zip(predictions, templates_list) if a != b]
        )
        entries = len(predictions)
        print(
            f"The score of the {self.lang} model is {score} with {misses} misses out of {entries} entries."
        )
        return

    def save(self):
        with open(f"{self.output_folder}/trained_model-{self.lang}.pickle", "wb") as file:
            pickle.dump(self.conjugator.model, file)
        return
