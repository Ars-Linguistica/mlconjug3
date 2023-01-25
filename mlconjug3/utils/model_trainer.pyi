import multiprocessing
import mlconjug3
import pickle
import numpy as np
from functools import partial
from time import time

from typing import Sequence, Mapping, Dict, Tuple, Optional, Union, Set, TextIO, Text, Any

class ConjugatorTrainer:
    def __init__(self, lang: str,
                 output_folder: str,
                 split_proportion: float,
                 feature_extractor: Optional[Any],
                 DataSet: mlconjug3.dataset.DataSet,
                 Model: mlconjug3.models.Model) -> None:
        ...

    def train(self) -> None:
        ...

    def predict(self) -> Sequence[Text]:
        ...

    def evaluate(self) -> None:
        ...

    def save(self) -> None:
        ...
