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

def costant_path(full_source:Path, first_w_index:int) -> Path:
    parent = Path("\\".join(full_source.parts[:first_w_index]))
    return parent

def wildcards(full_source:Path, first_w_index:int, last_w_index:int) -> str:
    wildcard = "\\".join(full_source.parts[first_w_index : last_w_index])
    return wildcard

def path_float_segment(fixed_source:Path, wildcard:str, w_indexes:list):
    w_index = -1
    while True:
        float_path = [Path(match.parts[w_indexes[w_index]])
                        for match in fixed_source.glob(wildcard)
                        ]

        if len(float_path) == len(set(float_path)):
            return w_index
        
        wildcard = wildcards(source, w_indexes[0], w_indexes[w_index])
        w_index -= 1
    

def copy(fixed_source:Path, fixed_dest:Path, wildcard:str, w_indexes:list):
    w_index = path_float_segment(fixed_source, wildcard, w_indexes)
    
    glob = [*fixed_source.glob(wildcard)]
    dest = fixed_dest

    for index, match in enumerate(glob):
        if len(match.parts) - 1 == w_indexes[w_index]:
            dest = fixed_dest / match.parts[w_indexes[w_index]]
        last_part = len(match.parts) - 1
        if last_part != w_indexes[w_index]:
            dest = Path(fixed_dest / match.parts[w_indexes[w_index]]) / match.name
        print(f"{index}: {match}    --->    {dest}")

def main():

    if is_filtered(source):
        wildcard_indexes = find_wildcard_indexes(source)
        # if wildcard_indexes > 2:
        const_path = costant_path(source, wildcard_indexes[0])
        last = wildcard_indexes[-1] + 1

        if wildcard_indexes[0] == wildcard_indexes[-1]:
            last = len(source.parts)
        wildcard = wildcards(source, wildcard_indexes[0], last)
        copy(const_path, destination, wildcard, wildcard_indexes)

if __name__ == '__main__':
    main()