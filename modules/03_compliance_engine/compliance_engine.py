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

def check_user_compliance(user_log):
    """
    Placeholder logic:
    Checks if all required actions are present in user_log (dict).
    """
    required_fields = ["session_completed", "feedback_given", "nutrition_logged"]
    missing = [field for field in required_fields if not user_log.get(field)]
    if missing:
        return False, f"Missing: {', '.join(missing)}"
    return True, "All compliance actions present."

if __name__ == "__main__":
    # Example: test user log
    test_log = {
        "session_completed": True,
        "feedback_given": False,
        "nutrition_logged": True
    }
    compliant, message = check_user_compliance(test_log)
    print("Compliant?" , compliant)
    print("Details:" , message)
