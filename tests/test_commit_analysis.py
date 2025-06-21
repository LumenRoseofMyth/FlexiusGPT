from modules.core.feedback.feedback_engine import _commit_motivation


def test_commit_motivation_levels():
    msgs = ["Awesome refactor", "wip fix"]
    level = _commit_motivation(msgs)
    assert level in {"high", "medium", "low"}
