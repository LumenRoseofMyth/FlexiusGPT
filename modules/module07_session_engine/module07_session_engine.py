"""Session engine core logic."""


def start_session(user_id: str) -> dict:
    return {"session": f"session_for_{user_id}"}
