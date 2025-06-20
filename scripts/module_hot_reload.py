import os
import sys
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from kernel.base_kernel import load_schemas, print_modules

MODULES_PATH = os.path.join(os.path.dirname(__file__), '..', 'modules')

class ModuleChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory:
            return
        if event.src_path.endswith('.md') or event.src_path.endswith('.py'):
            print(f"\nDetected change in: {event.src_path}")
            print("Reloading modules...")
            modules = load_schemas()
            print_modules(modules)
            print("Reload complete.\n")

if __name__ == "__main__":
    print(f"Watching {MODULES_PATH} for changes (hot reload enabled). Press Ctrl+C to exit.")
    event_handler = ModuleChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, MODULES_PATH, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
