import os
import yaml

MODULES_PATH = os.path.join(os.path.dirname(__file__), '..', 'modules')

def load_schemas():
    modules = []
    for mod_folder in sorted(os.listdir(MODULES_PATH)):
        mod_path = os.path.join(MODULES_PATH, mod_folder)
        schema_file = os.path.join(mod_path, 'schema.md')
        if os.path.isfile(schema_file):
            with open(schema_file, 'r', encoding='utf-8') as f:
                # Find YAML front matter between --- lines
                lines = f.read().splitlines()
                if lines[0].strip() == '---':
                    yaml_lines = []
                    for line in lines[1:]:
                        if line.strip() == '---':
                            break
                        yaml_lines.append(line)
                    schema = yaml.safe_load('\n'.join(yaml_lines))
                    modules.append({
                        "folder": mod_folder,
                        "schema": schema
                    })
    return modules

def print_modules(modules):
    print("Discovered modules and schemas:")
    for mod in modules:
        print(f"  {mod['folder']}: {mod['schema'].get('module_name','[NO NAME]')} ({mod['schema'].get('module_id','[NO ID]')})")

if __name__ == "__main__":
    modules = load_schemas()
    print_modules(modules)
