# @lock
"""
Custom core exceptions for FlexiusGPT routing.
"""

class CorePermissionError(PermissionError):
    """Raised when a call tries to touch protected core without override."""

class ModuleInterfaceError(ImportError):
    """Raised when a module or its run_module entry is missing."""

class PayloadValidationError(ValueError):
    """Raised when payload schema validation fails."""
