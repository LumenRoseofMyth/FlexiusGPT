import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from kernel.base_kernel import load_schemas

REQUIRED_FIELDS = ['module_name', 'module_id', 'description']

def check_compliance(schema):
    problems = []
    for field in REQUIRED_FIELDS:
        value = schema.get(field, None)
        if not value or (isinstance(value, str) and value.strip() == ""):
            problems.append(f"- Missing or empty: {field}")
        # If field is a list, also flag it (should be a string)
        if isinstance(value, list):
            problems.append(f"- Field '{field}' should be a string, not a list")
    return problems

def gpt_query(module_id=None, compliance=False):
    modules = load_schemas()
    if module_id:
        # Find by module_id (case-insensitive)
        found = [mod for mod in modules if mod['schema'].get('module_id','').lower() == module_id.lower()]
        if found:
            mod = found[0]
            schema = mod['schema']
            print(f"Module: {schema.get('module_name')}")
            print(f"ID: {schema.get('module_id')}")
            print(f"Description: {schema.get('description')}")
            if compliance:
                print("\nCompliance Check:")
                problems = check_compliance(schema)
                if problems:
                    for problem in problems:
                        print(problem)
                else:
                    print("✓ All required fields are present and valid.")
        else:
            print(f"No module found with ID: {module_id}")
    else:
        print("All modules:")
        for mod in modules:
            print(f"  {mod['schema'].get('module_id')} - {mod['schema'].get('module_name')}")
        print("\nTo get a specific module's info, run:\n  python -m adapters.gpt_adapter MODULE_ID [--compliance]")

if __name__ == "__main__":
    module_id = None
    compliance = False
    for arg in sys.argv[1:]:
        if arg.startswith('--'):
            if arg == '--compliance':
                compliance = True
        else:
            module_id = arg
    gpt_query(module_id, compliance)
