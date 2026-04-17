from typing import Optional, Sequence, Any
from sklearn.pipeline import Pipeline


class Model:
    pipeline: Pipeline
    language: Optional[str]

    def __init__(
        self,
        vectorizer: Optional[Any] = ...,
        feature_selector: Optional[Any] = ...,
        classifier: Optional[Any] = ...,
        language: Optional[str] = ...,
    ) -> None: ...

    def __repr__(self) -> str: ...

    def train(
        self,
        samples: Sequence[str],
        labels: Sequence[str],
    ) -> None: ...

    def predict(self, verbs: Sequence[str]) -> Sequence[str]: ...
