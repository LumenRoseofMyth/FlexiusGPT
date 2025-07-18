"""
Central orchestrator routing — Phase 3.
"""

from importlib import import_module
from typing import Any, Dict

from .exceptions import (
    CorePermissionError,
    ModuleInterfaceError,
    PayloadValidationError,
)
from .validator import validate_payload

PROTECTED_PREFIXES = ("core.", ".core", "infra.", ".infra", "_")


def _import_run(module_path: str):
    """Return `run_module` callable from a dotted module path."""
    try:
        module = import_module(module_path)
        return getattr(module, "run_module")
    except (ImportError, AttributeError) as exc:
        raise ModuleInterfaceError(f"run_module missing in {module_path}") from exc


def call_module_logic(
    module_name: str,
    payload: Dict[str, Any],
    *,
    override_protection: bool = False,
) -> Dict[str, Any]:
    """
    Entry-point for every plugin invocation.
    """
    # 1. schema validation
    try:
        validate_payload(payload)
    except ValueError as exc:
        raise PayloadValidationError(str(exc)) from None

    # 2. core protection
    if module_name.startswith(PROTECTED_PREFIXES) and not override_protection:
        raise CorePermissionError(
            f"Module '{module_name}' is protected; override_protection required."
        )

    # 3. dynamic import (expects modules.<name>.interface)
    interface_path = f"modules.{module_name}.interface"
    run_module = _import_run(interface_path)

    # 4. execute plugin
    return run_module(payload)
