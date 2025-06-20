import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def call_module_logic(module_id, action, user_log=None):
    module_path = os.path.join(os.path.dirname(__file__), '..', 'modules', module_id)
    logic_file = os.path.join(module_path, f"{module_id.split('_',1)[1]}.py")  # E.g. compliance_engine.py
    if not os.path.isfile(logic_file):
        print(f"No logic file found: {logic_file}")
        return

    import importlib.util
    spec = importlib.util.spec_from_file_location("module_logic", logic_file)
    module_logic = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module_logic)

    if hasattr(module_logic, action):
        func = getattr(module_logic, action)
        result = func(user_log) if user_log else func()
        print(f"Result from {action} in {module_id}: {result}")
    else:
        print(f"Action '{action}' not found in {logic_file}")

def run_workflow(workflow_name, user_log):
    if workflow_name == "full_compliance_check":
        modules_to_check = [
            ("03_compliance_engine", "check_user_compliance"),
            # Add more modules/actions here if desired, e.g.,
            # ("07_session_engine", "analyze_session"),
        ]
        results = []
        for module_id, action in modules_to_check:
            module_path = os.path.join(os.path.dirname(__file__), '..', 'modules', module_id)
            logic_file = os.path.join(module_path, f"{module_id.split('_',1)[1]}.py")
            if not os.path.isfile(logic_file):
                results.append((module_id, "No logic file"))
                continue
            import importlib.util
            spec = importlib.util.spec_from_file_location("module_logic", logic_file)
            module_logic = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module_logic)
            func = getattr(module_logic, action, None)
            if func:
                result = func(user_log)
                results.append((module_id, result))
            else:
                results.append((module_id, f"Action '{action}' not found"))
        print("Workflow results:")
        for mod_id, res in results:
            print(f"{mod_id}: {res}")
    else:
        print(f"Unknown workflow: {workflow_name}")

if __name__ == "__main__":
    if len(sys.argv) >= 3 and sys.argv[1] == "workflow":
        # Usage: python -m adapters.gpt_adapter workflow full_compliance_check '{"session_completed": true, ...}'
        workflow_name = sys.argv[2]
        user_log = json.loads(sys.argv[3]) if len(sys.argv) > 3 else {}
        run_workflow(workflow_name, user_log)
    else:
        # Existing single-module logic here
        # (You can leave your single-module code as is, or call your function as before)
        if len(sys.argv) > 1:
            module_id = sys.argv[1]
            action = sys.argv[2] if len(sys.argv) > 2 else None
            user_log = json.loads(sys.argv[3]) if len(sys.argv) > 3 else None
            call_module_logic(module_id, action, user_log)
        else:
            print("Usage:\n"
                  "  python -m adapters.gpt_adapter MODULE_ID ACTION [user_log_json]\n"
                  "  python -m adapters.gpt_adapter workflow WORKFLOW_NAME [user_log_json]")
