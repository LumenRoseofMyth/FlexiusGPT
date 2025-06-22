import os
from typing import Optional, Dict, List

def run(user_log: Optional[str] = None) -> None:
    print("🔍 Starting deep dive review of repository...")

    # === Step 1: Walk the Repo and Build Structure Index ===
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    structure_map: Dict[str, List[str]] = {}
    for root, _, files in os.walk(repo_root):
        rel_path = os.path.relpath(root, repo_root)
        structure_map[rel_path] = list(files)

    print(f"✅ Repository structure mapped. {len(structure_map)} directories found.")

    # === Step 2: Identify API integration layers ===
    connector_files: List[str] = []
    for path, file_list in structure_map.items():
        for file in file_list:
            file_str = file
            if "openapi" in file_str.lower() or file_str.endswith((".yaml", ".json")):
                connector_files.append(os.path.join(path, file))

    print(f"📡 Found {len(connector_files)} potential connector files:")
    for conn in connector_files:
        print(f" - {conn}")

    # === Step 3: Analyze FastAPI main setup ===
    main_api_path = os.path.join(repo_root, "api", "main.py")
    if not os.path.exists(main_api_path):
        print("❌ Could not find api/main.py. Review aborted.")
        return

    with open(main_api_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    connector_checkpoints = {
        "openapi": any("get_openapi" in l for l in lines),
        "plugin_meta": any("/.well-known" in l for l in lines),
        "api_key": any("X-API-KEY" in l for l in lines),
    }

    print("\n🧠 Connection Layer Checkpoints:")
    for k, v in connector_checkpoints.items():
        status = "✅ Present" if v else "⚠️ Missing"
        print(f" - {k}: {status}")

    # === Step 4: Suggest Next Upgrades ===
    print("\n🚀 Upgrade Suggestions:")
    if not connector_checkpoints["plugin_meta"]:
        print(" - Add StaticFiles mount for /.well-known for Custom GPT plugin compatibility.")
    if not connector_checkpoints["openapi"]:
        print(" - Define `custom_openapi()` to configure GPT-facing schema.")
    if not connector_checkpoints["api_key"]:
        print(" - Secure endpoints using X-API-KEY for authenticated access.")

    print("\n✅ Deep dive complete. Manual review may still be required for semantic integrity.")