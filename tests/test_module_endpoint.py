import os
from importlib import reload
from fastapi.testclient import TestClient

os.environ["FLEXIUSGPT_API_KEY"] = "testkey"
import api.main as main
reload(main)

client = TestClient(main.app)


def test_module_endpoint_success():
    resp = client.post(
        "/module",
        headers={"X-API-KEY": "testkey"},
        json={"module_id": "01_core_rules", "payload": {"action": "test_mode"}},
    )
    assert resp.status_code == 200
    assert resp.json()["success"] is True


def test_module_endpoint_requires_payload_dict():
    resp = client.post(
        "/module",
        headers={"X-API-KEY": "testkey"},
        json={"module_id": "01_core_rules", "action": "test_mode"},
    )
    assert resp.status_code in (400, 422)


def test_module_endpoint_missing_fields():
    resp = client.post(
        "/module",
        headers={"X-API-KEY": "testkey"},
        json={"module_id": "01_core_rules", "payload": {"foo": "bar"}},
    )
    assert resp.status_code == 422
    body = resp.json()
    assert "expected_schema" in body.get("detail", {})
