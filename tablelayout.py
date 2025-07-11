#tablelayout -i <target>
#This script will take target dir and get all files, sort them like this
#|target
#|--a               (file)
#|--b               (file)
#|--c               (file)
#|--|a              (folder)
#|  |--a            (file)
#|  |--b            (file)
#|  |--c            (file)
#|
#|--|b              (folder)
#|  |--a            (file)
#|  |--b            (file)
#|  |--|c           (folder)
#|     |--a         (file)
#|     |--b         (file)
#|     |--c         (file)
#...

import os
import argparse
from pathlib import Path

parser = argparse.ArgumentParser(description="Generate a table layout of all files in a directory.")
parser.add_argument("-i", help="Target directory", default=".")
args = parser.parse_args()

def write_file_table(base: Path, rel: Path, out: Path):
    abs = base / rel

    for file in sorted(abs.glob("*")):
        if file.is_file():
            with out.open("a", encoding="utf-8") as f:
                f.write(str(rel / file.name).replace("\\", "/") + "\n")

    for dir in sorted(abs.glob("*")):
        if dir.is_dir():
            write_file_table(base, rel / dir.name, out)

def main(input="."):
    target = Path(input).resolve()
    base = target.name
    parent = target.parent
    list_file = Path.cwd() / f"{base}.table.txt"

    try:
        list_file.unlink()
    except FileNotFoundError:
        pass

    write_file_table(parent, Path(base), list_file)
    print(f"File list written to: {list_file}")
    
main(args.i)

