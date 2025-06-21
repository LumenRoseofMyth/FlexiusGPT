from modules.core.twin.digital_twin_engine import DigitalTwin
from modules.core_tools.feedback_types import MultiModalFeedback


def test_volatility_and_burnout_prediction():
    twin = DigitalTwin({})
    metrics = [
        {"date": "d1", "metrics": {"lines_added": 100}, "hour": 9},
        {"date": "d2", "metrics": {"lines_added": 900}, "hour": 10},
        {"date": "d3", "metrics": {"lines_added": 1100}, "hour": 11},
    ]
    for m in metrics:
        twin.update(MultiModalFeedback(), {}, {}, metric=m)
    assert twin.state["meta"]["burnout_risk"] == "high"
    assert "circadian_peak" in twin.state["meta"]
