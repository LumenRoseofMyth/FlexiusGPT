from flexius_monorepo.core.exceptions import (
    CorePermissionError,
    ModuleInterfaceError,
    PayloadValidationError,
)


def test_exceptions():
    assert issubclass(PayloadValidationError, Exception)
    assert issubclass(CorePermissionError, Exception)
    assert issubclass(ModuleInterfaceError, Exception)
