import inspect
import functools
import typing as t
from fastapi import HTTPException
from pydantic import BaseModel, ValidationError, create_model


def pydantic_model_from_sig(fn: t.Callable[..., t.Any]) -> type[BaseModel]:
    """Build a pydantic model from a function signature (kw-only)."""
    hints = t.get_type_hints(fn)
    params = inspect.signature(fn).parameters
    fields: dict[str, tuple[type, t.Any]] = {}
    for name, param in params.items():
        if name == 'return' or param.kind is inspect.Parameter.VAR_POSITIONAL:
            continue
        if param.kind in (
            inspect.Parameter.KEYWORD_ONLY,
            inspect.Parameter.POSITIONAL_OR_KEYWORD,
        ):
            default = param.default if param.default is not inspect.Parameter.empty else ...
            fields[name] = (hints.get(name, t.Any), default)
    # For Pydantic v2, use __annotations__ and field defaults as keyword arguments
    model_name = fn.__name__.title() + "Model"
    annotations = {k: v[0] for k, v in fields.items()}
    field_defaults = {k: v[1] for k, v in fields.items() if v[1] is not ...}
    return create_model(model_name, __annotations__=annotations, **field_defaults)


def validate_payload(fn: t.Callable[..., t.Any]) -> t.Callable[..., t.Any]:
    Model = pydantic_model_from_sig(fn)

    @functools.wraps(fn)
    def wrapper(*, payload: dict[str, t.Any], **kw: dict[str, t.Any]):
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

    setattr(wrapper, "__payload_model__", Model)
    return wrapper
