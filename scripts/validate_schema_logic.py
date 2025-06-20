"""
Validate every modules/*/schema.md:

• YAML front-matter present
• Required keys: module_name, module_id, version, description
• Corresponding *.py contains run_module()

Exit code 1 on failure so CI can block bad commits.
"""
import pathlib, sys, yaml, importlib.util, re

ROOT = pathlib.Path(__file__).resolve().parents[1]
REQUIRED_KEYS = {"module_name", "module_id", "version", "description"}

def fail(msg):
    print(f"[FAIL] {msg}")
    sys.exit(1)

for schema in ROOT.glob("modules/*/schema.md"):
    raw = schema.read_text()
    # Split on lines with only '---'
    parts = re.split(r"^---\s*$", raw, flags=re.MULTILINE)
    if len(parts) < 3:
        fail(f"{schema}: Missing or malformed YAML front-matter (---)")
    yaml_block = parts[1]
    try:
        meta = yaml.safe_load(yaml_block)
    except Exception as e:
        fail(f"{schema}: YAML parse error: {e}")
    if not isinstance(meta, dict):
        fail(f"{schema}: YAML front-matter is not a dict")
    missing = REQUIRED_KEYS - meta.keys()
    if missing:
        fail(f"{schema}: Missing required keys: {', '.join(missing)}")
    # Check for corresponding .py file
    py_path = schema.parent / (schema.parent.name + ".py")
    if not py_path.exists():
        fail(f"{py_path}: Python module not found")
    # Check for run_module() in .py file
    spec = importlib.util.spec_from_file_location("mod", py_path)
    mod = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)
    except Exception as e:
        fail(f"{py_path}: Import error: {e}")
    if not hasattr(mod, "run_module"):
        fail(f"{py_path}: Missing run_module()")
    print(f"[OK] {schema}")

print("All schemas validated successfully.")