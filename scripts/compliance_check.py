import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from kernel.base_kernel import load_schemas

REQUIRED_FIELDS = ['module_name', 'module_id', 'description']

def check_module_compliance(mod):
    problems = []
    schema = mod['schema']
    for field in REQUIRED_FIELDS:
        value = schema.get(field, None)
        if not value or (isinstance(value, str) and value.strip() == ""):
            problems.append(f"- Missing or empty: {field}")
        if isinstance(value, list):
            problems.append(f"- Field '{field}' should be a string, not a list")
    return problems

if __name__ == "__main__":
    modules = load_schemas()
    errors = []
    for mod in modules:
        problems = check_module_compliance(mod)
        if problems:
            errors.append((mod['schema'].get('module_id'), mod['schema'].get('module_name'), problems))
    if errors:
        print("\n--- COMPLIANCE ERRORS FOUND ---")
        for module_id, module_name, problems in errors:
            print(f"{module_id} ({module_name}):")
            for problem in problems:
                print(f"  {problem}")
        print("\nPlease fix these errors before proceeding.")
        sys.exit(1)
    else:
        print("[OK] All modules are compliant. Ready for update, push, or automation.")

