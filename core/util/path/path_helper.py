from pathlib import Path
import os

class PathHelper:
    def __init__(self):
        pass

    @staticmethod
    def get_project_root_path() -> Path:
        return Path(__file__).parent.parent.parent.parent

    @staticmethod
    def create_directory(path):
        if not os.path.exists(path):
            os.makedirs(path)
        return path

    @staticmethod
    def create_file(path, name, content, extension):
        # create a new file with the given extension in the current directory
        if f".{extension}" in name:
            new_file_path = os.path.join(path, f"{name}")
        else:
            new_file_path = os.path.join(path, f"{name}.{extension}")
        with open(new_file_path, "w", encoding='utf-8') as f:
            f.write(content)
        return new_file_path
