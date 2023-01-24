"""
This module provides the ConjugatorTrainer class, a tool for training, evaluating,
and saving models for conjugating verbs in different languages.

The ConjugatorTrainer class allows the user to train a model for a specific language using the mlconjug3 library.
The user can also evaluate the model's performance and save the trained model for later use.

"""

import multiprocessing
import mlconjug3
import pickle
import numpy as np
from functools import partial
from time import time

class ConjugatorTrainer:
    """
    Initialize a ConjugatorTrainer instance.

    Args:
        lang (str): The language for which the model will be trained.
        output_folder (str): The directory where the trained model will be saved.
        split_proportion (float): The proportion of the data set to use for training.
        feature_extractor (obj): The feature extractor to use for the model.
        DataSet (class): The DataSet class from the mlconjug3 library.
        Model (obj): The model to be trained.
    """
    def __init__(self, lang, output_folder, split_proportion, feature_extractor, dataset, model):
        self.lang = lang
        self.output_folder = output_folder
        self.split_proportion = split_proportion
        self.feature_extractor = feature_extractor
        self.dataset = dataset
        self.model = model
        return

    def train(self):
        """
        Train the model using the specified parameters.
        """
        np.random.seed(42)

        # Initialize Data Set
        dataset = self.dataset(mlconjug3.Verbiste(language=self.lang))
        dataset.split_data(proportion=self.split_proportion)

        # Initialize Conjugator
        conjugator = mlconjug3.Conjugator(
            self.lang,
            feature_extractor=dataset.feature_extractor,
            model=self.model,
        )

        # Train Conjugator
        result = conjugator.model.train(dataset.verbs_list, dataset.templates_list)

        # Print training duration
        print(f"{self.lang} model trained on full data set in {result} seconds.")
        return

    def predict(self):
        """
        Make predictions using the trained model.

        Returns:
            list: A list of predictions for the conjugated verbs.
        """
        return self.conjugator.model.predict(self.dataset.verbs_list)

    def evaluate(self):
        """
        Evaluate the performance of the model's predictions.

        Prints the score of the model, with the number of misses out of the total number of entries.
        """
        predictions = self.conjugator.model.predict(self.dataset.verbs_list)
        score = len(
            [a == b for a, b in zip(predictions, self.dataset.templates_list) if a == b]
        ) / len(predictions)
        misses = len(
            [a != b for a, b in zip(predictions, self.dataset.templates_list) if a != b]
        )
        entries = len(predictions)
        print(
            f"The score of the {self.lang} model is {score} with {misses} misses out of {entries} entries."
        )
        return

    def save(self):
        """
        Save the trained conjugator model to the specified output folder.
        """
        with open(f"{self.output_folder}/trained_model-{self.lang}.pickle", "wb") as file:
            pickle.dump(self.conjugator.model, file)
        return
