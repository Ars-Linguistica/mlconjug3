from typing import Sequence, Any


def analyze_errors(
    lang: str,
    y_true: Sequence[int],
    y_pred: Sequence[int],
    inputs: Sequence[str],
    top_k: int = ...
) -> None: ...
