import os

def load_code(file_path: str) -> str:
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return str(file.read())
    else:
        return "File not found"