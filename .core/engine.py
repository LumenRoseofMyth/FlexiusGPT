# @lock
"""
Core engine stubs for FlexiusGPT.
"""

class BaseEngine:
    """Base class for core processing engines."""
    def process(self, *args, **kwargs):
        raise NotImplementedError
