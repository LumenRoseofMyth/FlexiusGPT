from modules.core.twin.digital_twin_engine import DigitalTwin
from modules.core_tools.feedback_types import MultiModalFeedback


def test_commit_volatility_and_circadian():
    twin = DigitalTwin({})
    fb = MultiModalFeedback(mood=5)
    for i in range(7):
        metric = {
            "type": "coding",
            "date": f"2025-06-{i+1:02d}",
            "metrics": {"pull_requests": i + 1, "lines_added": (i + 1) * 10},
            "data": {"commit_times": [f"2025-06-{i+1:02d}T0{i%5}:00:00"]},
        }
        twin.update(fb, None, {}, metric)

    meta = twin.state.get("meta", {})
    assert meta.get("commit_volatility") is not None
    assert meta.get("circadian_rhythm_hour") is not None

