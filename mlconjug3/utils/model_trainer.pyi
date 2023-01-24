import multiprocessing
import mlconjug3
import pickle
import numpy as np
from functools import partial
from time import time

class ConjugatorTrainer:
    def __init__(self, lang: str,
                 output_folder: str,
                 split_proportion: float,
                 feature_extractor: Optional[Any],
                 DataSet: mlconjug3.dataset.Dataset,
                 Model: mlconjug3.models.Model) -> None:
        ...

    def train(self) -> None:
        ...

    def predict(self) -> list:
        ...

    def evaluate(self) -> None:
        ...

    def save(self) -> None:
        ...
