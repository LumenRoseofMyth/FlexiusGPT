"""
Central core exceptions for FlexiusGPT.
"""


class PayloadValidationError(Exception):
    """Raised when the input payload fails schema validation."""


class CorePermissionError(Exception):
    """Raised when a caller tries to invoke protected core logic without override."""


class ModuleInterfaceError(Exception):
    """Raised when a module does not implement the required `run_module` interface."""
