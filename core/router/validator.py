import inspect
import functools
import typing as t
from fastapi import HTTPException
from pydantic import BaseModel, ValidationError, create_model


def pydantic_model_from_sig(fn: t.Callable) -> type[BaseModel]:
    """Build a pydantic model from a function signature (kw-only)."""
    hints = t.get_type_hints(fn)
    params = inspect.signature(fn).parameters
    fields = {}
    for name, param in params.items():
        if name == 'return' or param.kind is inspect.Parameter.VAR_POSITIONAL:
            continue
        if param.kind in (
            inspect.Parameter.KEYWORD_ONLY,
            inspect.Parameter.POSITIONAL_OR_KEYWORD,
        ):
            fields[name] = (hints.get(name, t.Any), ...)
    return create_model(fn.__name__.title() + "Model", **fields)


def validate_payload(fn: t.Callable):
    Model = pydantic_model_from_sig(fn)

    @functools.wraps(fn)
    def wrapper(*, payload: dict, **kw):
        try:
            data = Model(**payload)
        except ValidationError as e:
            sample = {
                name: f"<{info.get('type', 'value')}>"
                for name, info in Model.model_json_schema().get('properties', {}).items()
            }
            raise HTTPException(
                status_code=422,
                detail={
                    'errors': e.errors(),
                    'expected_schema': Model.model_json_schema().get('properties', {}),
                    'received_payload': payload,
                    'sample_payload': sample,
                },
            )
        return fn(**data.model_dump(), **kw)

    wrapper.__payload_model__ = Model
    return wrapper
