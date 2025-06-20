# codex_adapter.py
from kernel.base_kernel import load_schemas, print_modules

def codex_query():
    print("=== Codex Adapter Test ===")
    modules = load_schemas()
    print_modules(modules)
    print("=== Adapter Test Complete ===")

if __name__ == "__main__":
    codex_query()
