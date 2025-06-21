import os
import hashlib


def generate_codex_checksum(file_path):
    with open(file_path, 'rb') as f:
        data = f.read()
    return hashlib.sha256(data).hexdigest()
