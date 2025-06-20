import math
from collections import defaultdict
from typing import List, Tuple


def _tokenize(text: str) -> List[str]:
    return [tok.lower() for tok in text.split()]


def _vectorize(text: str) -> defaultdict[str, int]:
    vec: defaultdict[str, int] = defaultdict(int)
    for tok in _tokenize(text):
        vec[tok] += 1
    return vec


def _cosine(v1: defaultdict, v2: defaultdict) -> float:
    dot = sum(v1[k] * v2.get(k, 0) for k in v1)
    norm1 = math.sqrt(sum(v * v for v in v1.values()))
    norm2 = math.sqrt(sum(v * v for v in v2.values()))
    return 0.0 if norm1 * norm2 == 0 else dot / (norm1 * norm2)


class VectorStore:
    """In-memory bag-of-words store with cosine similarity."""

    def __init__(self):
        self._items: List[Tuple[str, defaultdict]] = []  # (raw, vec)

    def add(self, text: str):
        self._items.append((text, _vectorize(text)))

    def query(self, text: str, top_k: int = 3) -> List[str]:
        q_vec = _vectorize(text)
        scored = [(raw, _cosine(q_vec, vec)) for raw, vec in self._items]
        return [r for r, _ in sorted(scored, key=lambda t: t[1], reverse=True)][:top_k]
