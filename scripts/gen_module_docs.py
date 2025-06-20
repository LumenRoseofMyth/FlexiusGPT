import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from kernel.base_kernel import load_schemas

DOCS_FILE = os.path.join(os.path.dirname(__file__), '..', 'docs', 'MODULES.md')

def main():
    modules = load_schemas()
    with open(DOCS_FILE, 'w', encoding='utf-8') as f:
        f.write("# FlexiusGPT Modules Documentation\n\n")
        f.write("| Module ID | Name | Description |\n")
        f.write("|-----------|------|-------------|\n")
        for mod in modules:
            schema = mod['schema']
            f.write(f"| {schema.get('module_id')} | {schema.get('module_name')} | {schema.get('description').replace('|','&#124;')} |\n")
        f.write("\n---\n")
        for mod in modules:
            schema = mod['schema']
            f.write(f"## {schema.get('module_name')} ({schema.get('module_id')})\n\n")
            f.write(f"**Version:** {schema.get('version','N/A')}\n\n")
            f.write(f"**Description:** {schema.get('description')}\n\n")
            f.write(f"**Dependencies:** {schema.get('dependencies')}\n\n")
            f.write(f"**Input Schema:** {schema.get('input_schema')}\n\n")
            f.write(f"**Output Schema:** {schema.get('output_schema')}\n\n")
            f.write(f"**Compliance Tags:** {schema.get('compliance_tags')}\n\n")
            f.write(f"**Last Reviewed:** {schema.get('last_reviewed','N/A')}\n\n")
            f.write("---\n\n")
    print("Documentation generated at docs/MODULES.md")

if __name__ == "__main__":
    main()
