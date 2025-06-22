# @lock
"""
Central orchestrator routing — Phase 3.

Responsibilities
* Validate payload via .core.validator.validate_payload
* Enforce override rules on protected namespaces
* Dynamically import module interface
* Invoke run_module and propagate result / errors
"""
from importlib import import_module
from typing import Dict, Any

from .validator import validate_payload
from .exceptions import (
    CorePermissionError,
    ModuleInterfaceError,
    PayloadValidationError,
)

PROTECTED_PREFIXES = ("core.", ".core", "infra.", ".infra", "_")


def _import_run(module_path: str):
    """Return run_module callable from a dotted module path."""
    try:
        mod = import_module(module_path)
        return getattr(mod, "run_module")
    except (ImportError, AttributeError) as exc:
        message = f"run_module missing in {module_path}"
        raise ModuleInterfaceError(message) from exc


def call_module_logic(
    module_name: str,
    payload: Dict[str, Any],
    *,
    override_protection: bool = False,
) -> Dict[str, Any]:
    """
    Entry-point for every plugin invocation.

    Parameters
    ----------
    module_name : str
        Name under `modules.` (e.g. "module01" or "01_core_rules").
    payload : dict
        Must satisfy schema in .core.validator.
    override_protection : bool
        True only when caller is explicitly allowed to touch protected core.

    Returns
    -------
    dict
        Whatever the plugin returns.

    Raises
    ------
    PayloadValidationError, CorePermissionError, ModuleInterfaceError
    """
    # 1. schema validation
    try:
        validate_payload(payload)
    except ValueError as exc:
        raise PayloadValidationError(str(exc)) from None

    # 2. core protection
    if module_name.startswith(PROTECTED_PREFIXES) and not override_protection:
        msg = (
            "Module '" + module_name + "' is protected; "
            "override_protection required."
        )
        raise CorePermissionError(msg)

    # 3. dynamic import (expects modules.<name>.interface)
    interface_path = f"modules.{module_name}.interface"
    run_module = _import_run(interface_path)

    # 4. execute plugin
    return run_module(payload)
