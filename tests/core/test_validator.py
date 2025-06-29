import pytest
from core.validator import validate_payload


def test_valid_payload():
    valid = {"payload": {"action": "process", "data": {}}}
    assert validate_payload(valid) is None


def test_invalid_payload_missing_keys():
    with pytest.raises(ValueError):
        validate_payload({"payload": {"data": {}}})


def test_invalid_payload_extra_keys():
    with pytest.raises(ValueError):
        validate_payload({"payload": {"action": "run", "data": {}, "extra": 1}})
