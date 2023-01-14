import abc
import joblib
import numpy as np
import pickle
from typing import Dict, List, Tuple
from zipfile import ZipFile
from functools import partial

class LanguageConjugator(abc.ABC):
    """
    Abstract class for all Language Conjugators.
    """
    def __init__(self, lang: str, model: 'Model') -> None:
        self.lang = lang
        self.model = model

    @abc.abstractmethod
    def train(self, input_data: List[str], labels: List[str]) -> None:
        pass

    @abc.abstractmethod
    def predict(self, input_data: List[str]) -> List[str]:
        pass

class Model:
    """
    Class to handle models
    """
    def __init__(self, vectorizer: 'Vectorizer', feature_reductor: 'FeatureReductor', classifier: 'Classifier') -> None:
        self.vectorizer = vectorizer
        self.feature_reductor = feature_reductor
        self.classifier = classifier

    def train(self, input_data: List[str], labels: List[str]) -> None:
        X = self.vectorizer.transform(input_data)
        X = self.feature_reductor.transform(X)
        self.classifier.fit(X, labels)

    def predict(self, input_data: List[str]) -> List[str]:
        X = self.vectorizer.transform(input_data)
        X = self.feature_reductor.transform(X)
        return self.classifier.predict(X)


class Vectorizer:
    """
    Class to handle vectorization of data
    """
    def __init__(self, analyzer: callable, binary: bool = True) -> None:
        self.analyzer = analyzer
        self.binary = binary

    def transform(self, input_data: List[str]) -> List[List[int]]:
        pass

class FeatureReductor:
    """
    Class to handle feature reduction
    """
    def __init__(self, reductor: 'Reductor') -> None:
        self.reductor = reductor

    def transform(self, input_data: List[List[int]]) -> List[List[int]]:
        pass

class Classifier:
    """
        Abstract class for all classifiers.
    """
    def __init__(self) -> None:
        pass

    @abc.abstractmethod
    def fit(self, input_data: List[List[int]], labels: List[str]) -> None:
        pass

    @abc.abstractmethod
    def predict(self, input_data: List[List[int]]) -> List[str]:
        pass

class VerbisteConjugator(LanguageConjugator):
    """
    Conjugator class that uses the Verbiste library
    """
    def __init__(self, lang: str, model: Model, verbiste: 'Verbiste') -> None:
        super().__init__(lang, model)
        self.verbiste = verbiste

    def train(self, input_data: List[str], labels: List[str]) -> None:
        verbs_list, templates_list = self.verbiste.conjugate(input_data)
        self.model.train(verbs_list, templates_list)

    def predict(self, input_data: List[str]) -> List[str]:
        verbs_list, _ = self.verbiste.conjugate(input_data)
        return self.model.predict(verbs_list)

class ConjugManagerConjugator(LanguageConjugator):
    """
    Conjugator class that uses the ConjugManager library
    """
    def __init__(self, lang: str, model: Model, conjug_manager: 'ConjugManager') -> None:
        super().__init__(lang, model)
        self.conjug_manager = conjug_manager

    def train(self, input_data: List[str], labels: List[str]) -> None:
        verbs_list, templates_list = self.conjug_manager.conjugate(input_data)
        self.model.train(verbs_list, templates_list)

    def predict(self, input_data: List[str]) -> List[str]:
        verbs_list, _ = self.conjug_manager.conjugate(input_data)
        return self.model.predict(verbs_list)

class DataSet:
    """
    Class to handle dataset
    """
    def __init__(self, verbs: List[str], conjugator: LanguageConjugator) -> None:
        self.verbs = verbs
        self.conjugator = conjugator

    def split_data(self, proportion: float) -> None:
        pass

    def train(self) -> None:
        pass

    def predict(self) -> None:
        pass

class MLConjug:
    """
    Main class for the user to interact with the package.
    """
    def __init__(self, lang: str, model_path: str = None) -> None:
        self.lang = lang
        self.vectorizer = CountVectorizer(analyzer=partial(extract_verb_features, lang=lang, ngram_range=(2, 7)), binary=True)
        self.feature_reductor = SelectFromModel(LinearSVC(penalty="l1", max_iter=12000, dual=    false, verbose=0))
        self.classifier = SGDClassifier(loss="log", penalty='elasticnet', l1_ratio=0.15, max_iter=40000, alpha=1e-5, verbose=0)
        self.model = Model(self.vectorizer, self.feature_reductor, self.classifier)
        if model_path is not None:
            self.load_model(model_path)
        self.conjugator = None
        if 'Verbiste' in globals():
            self.conjugator = VerbisteConjugator(lang, self.model, Verbiste(language=lang))
        elif 'ConjugManager' in globals():
            self.conjugator = ConjugManagerConjugator(lang, self.model, ConjugManager(language=lang))

    def train(self, input_data: List[str], labels: List[str]) -> None:
        if self.conjugator is None:
            raise ValueError("No conjugation library was found. Make sure Verbiste or ConjugManager is installed.")
        self.conjugator.train(input_data, labels)

    def predict(self, input_data: List[str]) -> List[str]:
        return self.conjugator.predict(input_data)

    def save_model(self, model_path: str) -> None:
        model_data = {'vectorizer': self.vectorizer, 'feature_reductor': self.feature_reductor, 'classifier': self.classifier}
        with ZipFile(model_path, 'w') as zipf:
            for key in model_data:
                filename = key + '.pkl'
                with open(filename, 'wb') as f:
                    pickle.dump(model_data[key], f)
                zipf.write(filename)

    def load_model(self, model_path: str) -> None:
        with ZipFile(model_path, 'r') as zipf:
            zipf.extractall()
            for key in ['vectorizer', 'feature_reductor', 'classifier']:
                filename = key + '.pkl'
                with open(filename, 'rb') as f:
                    model_data = pickle.load(    false, verbose=0))
        self.classifier = SGDClassifier(loss="log", penalty='elasticnet', l1_ratio=0.15, max_iter=40000, alpha=1e-5, verbose=0)
        self.model = Model(self.vectorizer, self.feature_reductor, self.classifier)
        if model_path is not None:
            self.load_model(model_path)
        self.conjugator = None
        if 'Verbiste' in globals():
            self.conjugator = VerbisteConjugator(lang, self.model, Verbiste(language=lang))
        elif 'ConjugManager' in globals():
            self.conjugator = ConjugManagerConjugator(lang, self.model, ConjugManager(language=lang))

    def train(self, input_data: List[str], labels: List[str]) -> None:
        if self.conjugator is None:
            raise ValueError("No conjugation library was found. Make sure Verbiste or ConjugManager is installed.")
        self.conjugator.train(input_data, labels)

    def predict(self, input_data: List[str]) -> List[str]:
        return self.conjugator.predict(input_data)

    def save_model(self, model_path: str) -> None:
        model_data = {'vectorizer': self.vectorizer, 'feature_reductor': self.feature_reductor, 'classifier': self.classifier}
        with ZipFile(model_path, 'w') as zipf:
            for key in model_data:
                filename = key + '.pkl'
                with open(filename, 'wb') as f:
                    pickle.dump(model_data[key], f)
                zipf.write(filename)

    def load_model(self, model_path: str) -> None:
        with ZipFile(model_path, 'r') as zipf:
            zipf.extractall()
            for key in ['vectorizer', 'feature_reductor', 'classifier']:
                filename = key + '.pkl'
                with open(filename, 'rb') as f:
                    model_data = pickle.load(



        

