# @lock
"""
Core package init.

Creates a public alias 'core' so `import core.engine`
works although the physical directory is `.core`.
"""
import sys as _sys

_sys.modules["core"] = _sys.modules[__name__]
