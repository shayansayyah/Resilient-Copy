from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

source = Path(os.getenv("PATH"))
destination = Path(os.getenv("DEST"))

FILTER_CHARS = '*?'

def is_filtered(full_source:Path) -> bool:
    return any(char in str(full_source) for char in FILTER_CHARS)

def find_wildcard_indexes(full_source:Path) -> int:
    indexes = set()
    for index, part in enumerate(full_source.parts):
        for char in part:
            if char in FILTER_CHARS:
                indexes.add(index)
    return sorted(indexes)

def costant_path(full_source:Path, index:int) -> Path:
    parent = Path("\\".join(full_source.parts[:index]))
    return parent

def wildcards(full_source:Path, first:int, last:int) -> str:
    wildcard = "\\".join(full_source.parts[first:last])
    return wildcard

def path_float_segment(fixed_source:Path, wildcard:str, w_indexes:list, w_index:int):
    
    float_path = [Path(directory.parts[w_indexes[w_index]])
            for directory in fixed_source.glob(wildcard)
            if directory.is_dir()]

    if len(float_path) == len(set(float_path)):
        return w_index
    
    wildcard = wildcards(source, w_indexes[0], w_indexes[w_index])
    w_index -= 1
    
    return path_float_segment(fixed_source, wildcard, w_indexes, w_index)

def copy(fixed_source:Path, fixed_dest:Path, wildcard:str, w_indexes:list):
    w_index = path_float_segment(fixed_source, wildcard, w_indexes, -1)
    glob = [*fixed_source.glob(wildcard)]
    for index, directory in enumerate(glob):
        f = Path(fixed_dest / directory.parts[w_indexes[w_index]])
        j = len(directory.parts) - 1
        if j != w_indexes[w_index]:
            f = Path(fixed_dest / directory.parts[w_indexes[w_index]]) / directory.name
        
        print(f"{index}: {directory}    --->    {f}")

def main():

    if is_filtered(source):
        wildcard_indexes = find_wildcard_indexes(source)
        const_path = costant_path(source, wildcard_indexes[0])
        last = wildcard_indexes[-1] + 1

        if wildcard_indexes[0] == wildcard_indexes[-1]:
            last = len(source.parts)
        wildcard = wildcards(source, wildcard_indexes[0], last)
        copy(const_path, destination, wildcard, wildcard_indexes)

if __name__ == '__main__':
    main()