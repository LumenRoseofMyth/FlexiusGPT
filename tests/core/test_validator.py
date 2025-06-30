REQUIRED_KEYS = {"action", "data"}
ALLOWED_KEYS = REQUIRED_KEYS  # Adjust this if additional optional keys are allowed


def validate_payload(input: dict) -> None:
    if "payload" not in input:
        raise ValueError("Missing 'payload' key")

    payload = input["payload"]

    missing = REQUIRED_KEYS - payload.keys()
    if missing:
        raise ValueError(f"Missing keys in payload: {missing}")

    extra = payload.keys() - ALLOWED_KEYS
    if extra:
        raise ValueError(f"Unexpected keys in payload: {extra}")
