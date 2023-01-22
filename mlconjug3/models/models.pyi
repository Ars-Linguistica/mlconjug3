from typing import Optional, Mapping, List, Sequence, DefaultDict, Any, Tuple, Type, AbstractSet, Union
from mlconjug3.feature_extractor import extract_verb_features
from sklearn.pipeline import Pipeline


class Model:
    pipeline: Pipeline = ...
    language: str = ...
    def __init__(self,
                 vectorizer: Optional[Any] = ...,
                 feature_selector: Optional[Any] = ...,
                 classifier: Optional[Any] = ...,
                 language: Optional[str] = ...
                 ) -> None: ...

    def __repr__(self) -> str: ...

    def train(self,
              samples: Sequence[str],
              labels: Sequence[int],
              ) -> None: ...

    def predict(self,
                verbs: Sequence[str]
                ) -> Sequence[int]: ...
      
