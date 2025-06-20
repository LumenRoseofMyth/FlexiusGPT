import os
import yaml

SCHEMA_FILE = os.path.join(os.path.dirname(__file__), "schema.md")

def load_schema():
    with open(SCHEMA_FILE, 'r', encoding='utf-8') as f:
        lines = f.read().splitlines()
        if lines[0].strip() == '---':
            yaml_lines = []
            for line in lines[1:]:
                if line.strip() == '---':
                    break
                yaml_lines.append(line)
            return yaml.safe_load('\n'.join(yaml_lines))
    return {}

def check_user_compliance(user_log: dict) -> tuple:
    """
    Validates whether all required compliance events were completed.

    Args:
        user_log (dict): Dictionary with boolean keys:
            - session_completed
            - feedback_given
            - nutrition_logged

    Returns:
        tuple: (bool, str)
            - True if compliant, False otherwise
            - Message indicating status or missing elements
    """
    required = ["session_completed", "feedback_given", "nutrition_logged"]
    missing = [key for key in required if not user_log.get(key, False)]

    if not missing:
        return True, "All compliance actions present."
    else:
        return False, f"Missing: {', '.join(missing)}"


if __name__ == "__main__":
    # For local CLI testing
    test_log = {
        "session_completed": True,
        "feedback_given": False,
        "nutrition_logged": True
    }
    print(check_user_compliance(test_log))