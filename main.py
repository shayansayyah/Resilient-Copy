from pathlib import Path
import subprocess

FILTER_CHARS = '*?['

def is_filtered(full_source:Path) -> bool:
    cleaned = str(full_source).replace("[[]", "").replace("[]]", "")
    return any(char in cleaned for char in FILTER_CHARS)

def find_wildcard_indexes(full_source:Path) -> list[int]:
    indexes = set()
    for index, part in enumerate(full_source.parts):
        cleaned = part.replace("[[]", "").replace("[]]", "")
        for char in cleaned:
            if char in FILTER_CHARS:
                indexes.add(index)
    return sorted(indexes)

def costant_path(full_source:Path, first_w_index:int) -> Path:
    parent = Path("\\".join(full_source.parts[:first_w_index]))
    return parent

def wildcards(full_source:Path, first_w_index:int, last_w_index:int) -> str:
    wildcard = "\\".join(full_source.parts[first_w_index : last_w_index])
    return wildcard

def path_float_segment(full_source:Path ,fixed_source:Path, w_indexes:list):

    f_index = w_indexes[0]
    for w_index in w_indexes:
        wildcard = wildcards(full_source, w_indexes[0], w_index + 1)

        matches = []
        for match in fixed_source.glob(wildcard):

            if w_index == w_indexes[-1]:
                matches.append(Path(match.parts[w_index]))
                continue
            
            if match.is_dir():
                matches.append(Path(match.parts[w_index]))

        if len(matches) == len(set(matches)):
            f_index = w_index

    return f_index

def copy(command:list):
    coping = subprocess.Popen(command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True)
    out, err = coping.communicate()
    print(f"Errors: {err}\n Stdout: {out}")


def make_floating_dir(fixed_source:Path, fixed_dest:Path, wildcard:str, floating_index:int):

    glob = [*fixed_source.glob(wildcard)]
    for match in glob:

        last_index = len(match.parts)

        if match.is_file():
            last_index -= 1

        floating_dest = wildcards(match, floating_index, last_index)
        dest = fixed_dest / floating_dest

        if not dest.exists():
            dest.mkdir(parents=True)
        command = ['robocopy', match, dest, '/E']

        if match.is_file():
            command = ['robocopy', fixed_source / floating_dest, dest, match.name]

        copy(command)
                    

def main():
    manual = """
---------------------------------------------------------
|  You can use below wildcards only in source path!     |
|  Example: C:/Users/*/ -->  C:/Users/public/           |
|                       -->  C:/Users/Default/          |
---------------------------------------------------------
|    *	    |   Any number of chars (not crossing /)    |
|    ?	    |   Exactly one char                        |
|    [abc]  |   One char from the set a, b, or c        |
|    [a-z]  |   One char in the range a–z               |
|    [1-9]  |   One integer in the range 1-9            |
|    [!abc] |   One char not in the set (also [^abc])   |
---------------------------------------------------------
|  For literal '[' and ']' use '[[]' and '[]]' .        |
|  Example: C:/Users/[[]bob[]]/ -->  C:/Users/[bob]/    |
---------------------------------------------------------

"""
    print(manual)
    source = Path(input("Source path: "))
    destination = Path(input("Destination path: "))
    
    if is_filtered(source):
        wildcard_indexes = find_wildcard_indexes(source) # sorted
        first_w_index = wildcard_indexes[0]
        last_w_index = wildcard_indexes[-1] + 1
        if len(wildcard_indexes) == 1:
            last_w_index = len(source.parts)

        fixed_source = costant_path(source, first_w_index)
        wildcard = wildcards(source, first_w_index, last_w_index)
        floating_index = path_float_segment(source, fixed_source, wildcard_indexes)
        make_floating_dir(fixed_source, destination, wildcard, floating_index)

    else:
        command = ['robocopy', source, destination, '/E']
        copy(command)

if __name__ == '__main__':
    main()