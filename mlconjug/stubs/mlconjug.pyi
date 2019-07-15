from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_selection.from_model import SelectFromModel
from sklearn.linear_model.stochastic_gradient import SGDClassifier
from typing import Dict


class Conjugator:
    def __init__(self, language: str = ..., model: None = ...) -> None: ...
    def set_model(self, model: Model) -> None: ...


class DataSet:
    def __init__(self, verbs_dict: Dict[str, Dict[str, str]]) -> None: ...
    def construct_dict_conjug(self) -> None: ...
    def split_data(self, threshold: int = ..., proportion: float = ...) -> None: ...


class Model:
    def __init__(
        self,
        vectorizer: Optional[CountVectorizer] = ...,
        feature_selector: Optional[SelectFromModel] = ...,
        classifier: Optional[SGDClassifier] = ...,
        language: None = ...
    ) -> None: ...
