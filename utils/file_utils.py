import os
from typing import List


def get_files_recursively(directory: str) -> List[str]:
    files = []
    dirs = os.listdir(directory)
    for d in dirs:
        path = os.path.join(directory, d)
        if os.path.isfile(path):
            files.append(path)
        else:
            files.extend(get_files_recursively(path))
    return files
