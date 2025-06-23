import os


def test_all_core_files_have_lock():
    locked_paths = [".core", "infra/secure"]
    bad_files = []

    for path in locked_paths:
        for root, _, files in os.walk(path):
            for f in files:
                if f.startswith(".") or f.endswith(".gitkeep"):
                    continue
                full_path = os.path.join(root, f)
                with open(full_path, "r", encoding="utf-8") as file:
                    first_line = file.readline().strip()
                    if first_line != "# @lock":
                        bad_files.append(full_path)

    assert not bad_files, f"Missing @lock in: {bad_files}"
