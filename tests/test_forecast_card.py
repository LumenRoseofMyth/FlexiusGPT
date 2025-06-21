from modules.core.feedback.feedback_engine import (
    init_digital_twin,
    generate_forecast_card,
    process_feedback,
)


def test_forecast_card(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    init_digital_twin({})
    process_feedback({}, {"mood": 5, "fatigue": 1}, {}, {})
    card = generate_forecast_card()
    assert "Weekly Forecast" in card
    assert (tmp_path / "out").exists()
