from collections import defaultdict
from typing import Callable, Dict


class ToolRegistry:
    """Global registry of callable tools."""

    _TOOLS: Dict[str, Callable] = {}

    @classmethod
    def register(cls, name: str):
        def decorator(fn: Callable):
            cls._TOOLS[name] = fn
            return fn

        return decorator

    @classmethod
    def get(cls, name: str) -> Callable | None:
        return cls._TOOLS.get(name)

    @classmethod
    def list(cls):
        return list(cls._TOOLS.keys())
