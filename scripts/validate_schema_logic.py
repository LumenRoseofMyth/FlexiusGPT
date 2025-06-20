"""
Validate every modules/*/schema.md:

• YAML front-matter present
• Required keys: module_name, module_id, version, description
• Corresponding *.py contains run_module()

Exit code 1 on failure so CI can block bad commits.
"""
import pathlib, sys, yaml, importlib.util, re

ROOT = pathlib.Path(__file__).resolve().parents[1]
MODS = ROOT / "modules"
REQ  = {"module_name","module_id","version","description"}
errors = []

for schema in MODS.rglob("schema.md"):
    mod_dir = schema.parent
    raw = schema.read_text(encoding="utf-8")
    if not raw.lstrip().startswith("---"):
        errors.append((mod_dir.name, "Missing YAML fence"))
        continue
    yaml_block = re.split(r"^---\\s*$", raw, flags=re.M)[1]
    try:
        meta = yaml.safe_load(yaml_block)
    except Exception as e:
        errors.append((mod_dir.name, f"YAML error: {e}"))
        continue
    missing = REQ - meta.keys()
    if missing:
        errors.append((mod_dir.name, f"Missing keys: {', '.join(missing)}"))
    logic_py = next(mod_dir.glob("*.py"))
    spec = importlib.util.spec_from_file_location("mod", logic_py)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    if not hasattr(mod, "run_module"):
        errors.append((mod_dir.name, "run_module() not found"))

if errors:
    print("Validation failed:")
    for mod, msg in errors:
        print(f"  – {mod}: {msg}")
    sys.exit(1)

print("✅  All schemas & logic files valid.")
