import os

REQUIRED_FILES = [
    "core/CORE_RULES.txt",
    "core/PHASE_MANAGER.txt",
    "core/SESSION_ENGINE.txt",
    "core/SAFETY_OVERRIDES.txt",
    "core/COMPLIANCE_ENGINE.txt",
    "core/USER_PROFILE.txt"
]

def test_himks_core_files_exist():
    for path in REQUIRED_FILES:
        assert os.path.exists(path), f"Missing: {path}"

