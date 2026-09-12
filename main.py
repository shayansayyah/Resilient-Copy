import subprocess
from pathlib import Path
from dotenv import load_dotenv
import os

FILTER_CHARS = '*?'

def is_filtered(path:Path) -> bool:
    return any(char in str(path) for char in FILTER_CHARS)

def find_filter_index(path:Path) -> int:
    for index, part in enumerate(path.parts):
        for char in part:
            if char in FILTER_CHARS:
                return index

def costant_path(path:Path, index:int) -> Path:
    parent = Path("\\".join(path.parts[:index]))
    return parent

def wildcard(path:Path, index:int) -> str:
    wildcard = "\\".join(path.parts[index:])
    return wildcard

def main():
    load_dotenv()

    source = Path(os.getenv("PATH")) #Path(input("path: ").strip())
    destination = Path(os.getenv("DEST"))

    if is_filtered(source):
        filter_index = find_filter_index(source)
        const_path = costant_path(source, filter_index)
        w_card = wildcard(source, filter_index)




if __name__ == '__main__':
    main()
