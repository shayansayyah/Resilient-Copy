import subprocess
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

sou = Path(os.getenv("PATH")) #Path(input("path: ").strip())
dest = Path(os.getenv("DEST"))

FILTER_CHARS = '*?'

def is_filtered(path:Path) -> bool:
    return any(char in str(path) for char in FILTER_CHARS)


def find_filter_index(path:Path) -> int:
    indexes = set()
    for index, part in enumerate(path.parts):
        for char in part:
            if char in FILTER_CHARS:
                indexes.add(index)
    return sorted(indexes)

def costant_path(path:Path, index:int) -> Path:
    parent = Path("\\".join(path.parts[:index]))
    return parent

def wildcard(path:Path, first:int, last:int) -> str:
    wildcard = "\\".join(path.parts[first:last])
    return wildcard

def destination(source:Path, desti:Path, wild:str, i:int, indexes:list):
    l = [Path(directory.parts[indexes[i]]) for directory in source.glob(wild) if directory.is_dir()]
    s = [l.count(Path(directory.parts[indexes[i]])) == 1 for directory in source.glob(wild) if directory.is_dir()]
    p = all(s)
    
    if p:
        return i, l
    
    w = wildcard(sou, indexes[0], indexes[i])
    i = i -1
    return destination(source, desti, w, i, indexes)

def copy(source:Path, desti:Path, wildcard:str, indexes:list):
    i, l = destination(source, desti, wildcard, -1, indexes)
    glob = [*source.glob(wildcard)]
    for index, directory in enumerate(glob):
        # print(f"{index + 1}: {desti / directory}")
        f = Path(desti / directory.parts[indexes[i]])
        j = len(directory.parts) - 1
        if j != indexes[i]:
            f = Path(desti / directory.parts[indexes[i]]) / directory.name
        
        print(f"{index}: {directory}    --->    {f}")

def main():

    if is_filtered(sou):
        filter_indexes = find_filter_index(sou)
        const_path = costant_path(sou, filter_indexes[0])
        last = filter_indexes[-1] + 1

        if filter_indexes[0] == filter_indexes[-1]:
            last = len(sou.parts)
        w_card = wildcard(sou, filter_indexes[0], last)
        copy(const_path, dest, w_card, filter_indexes)

if __name__ == '__main__':
    main()
