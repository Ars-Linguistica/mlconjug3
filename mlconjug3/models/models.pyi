from typing import Optional, Sequence, Any
from sklearn.pipeline import Pipeline


class Model:
    pipeline: Pipeline
    language: Optional[str]

    def __init__(
        self,
        vectorizer: Optional[Any] = ...,
        classifier: Optional[Any] = ...,
        language: Optional[str] = ...,
    ) -> None: ...

    def __repr__(self) -> str: ...

    def train(
        self,
        samples: Sequence[str],
        labels: Sequence[int],
        sample_weight: Optional[Sequence[float]] = ...,
    ) -> "Model": ...

    def predict(self, verbs: Sequence[str]) -> Sequence[int]: ...

    def predict_proba(self, verbs: Sequence[str]) -> Any: ...
