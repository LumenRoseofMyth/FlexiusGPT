import sys
import os
import json
import importlib.util

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from adapters.gpt_adapter import call_module_logic, run_workflow

# Define your test cases for modules
TEST_CASES = [
    {
        "module_id": "03_compliance_engine",
        "action": "check_user_compliance",
        "input": {"session_completed": True, "feedback_given": True, "nutrition_logged": True},
        "expected": (True, "All compliance actions present."),
    },
    {
        "module_id": "03_compliance_engine",
        "action": "check_user_compliance",
        "input": {"session_completed": True, "feedback_given": False, "nutrition_logged": True},
        "expected": (False, "Missing: feedback_given"),
    },
    # Add more module/action/input/expected test cases here!
]

# Define workflow test cases
WORKFLOW_TESTS = [
    {
        "workflow": "full_compliance_check",
        "input": {"session_completed": True, "feedback_given": True, "nutrition_logged": True},
        "expected": [
            ("03_compliance_engine", (True, "All compliance actions present.")),
            # add more as you build!
        ]
    }
]

def test_module_logic():
    print("\n--- Module Analytic Tests ---")
    for test in TEST_CASES:
        print(f"\n{test['module_id']}.{test['action']}({test['input']})")
        # Directly import and call function for assert/compare
        module_path = os.path.join(os.path.dirname(__file__), '..', 'modules', test['module_id'])
        logic_file = os.path.join(module_path, f"{test['module_id'].split('_',1)[1]}.py")
        if not os.path.isfile(logic_file):
            print(f"❌ No logic file found: {logic_file}")
            continue
        spec = importlib.util.spec_from_file_location("module_logic", logic_file)
        module_logic = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module_logic)
        func = getattr(module_logic, test['action'], None)
        if not func:
            print(f"❌ No function '{test['action']}' in {logic_file}")
            continue
        result = func(test['input'])
        if result == test['expected']:
            print(f"✅ PASS: Output matches expected: {result}")
        else:
            print(f"❌ FAIL: Got {result}, expected {test['expected']}")

def test_workflows():
    print("\n--- Workflow Analytic Tests ---")
    for test in WORKFLOW_TESTS:
        print(f"\nworkflow: {test['workflow']} input={test['input']}")
        # We use the run_workflow function and capture printed output by monkeypatching 'print'
        import io
        from contextlib import redirect_stdout
        f = io.StringIO()
        with redirect_stdout(f):
            run_workflow(test['workflow'], test['input'])
        out = f.getvalue()
        # Just print, or add parsing if you want auto-PASS/FAIL for workflow results
        print(out.strip())

if __name__ == "__main__":
    print("\n=== HIMKS Analytic Test Suite ===")
    test_module_logic()
    test_workflows()
    print("\n=== Test Suite Complete ===")
