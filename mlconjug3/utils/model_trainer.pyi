import multiprocessing
import mlconjug3
import pickle
import numpy as np
from functools import partial
from time import time

class ConjugatorTrainer:
    def __init__(self, lang:str, output_folder:str, split_proportion:float, feature_extractor, DataSet, Model) -> None:
        ...

    def train(self) -> None:
        ...

    def predict(self, verbs_list:list) -> list:
        ...

    def evaluate(self, predictions:list, templates_list:list) -> None:
        ...

    def save(self) -> None:
        ...
