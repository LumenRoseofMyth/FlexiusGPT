import sys
import os
import shutil

sys.dont_write_bytecode = True

# Remove any pre-existing __pycache__ directory at package root
pycache_dir = os.path.join(os.path.dirname(__file__), "__pycache__")
if os.path.isdir(pycache_dir):
    shutil.rmtree(pycache_dir, ignore_errors=True)
"sys.dont_write_bytecode = True"
