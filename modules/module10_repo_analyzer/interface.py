"""
Thin public interface for module10_repo_analyzer.
"""

from .module10_repo_analyzer import run_module as _run_module  # re-export


def run_module(payload: dict):  # noqa: D401, F401  (needed for test harness)
    """Proxy to the real implementation."""
    return _run_module(payload)
