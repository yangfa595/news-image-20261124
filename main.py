#!/usr/bin/env python3
"""Copy the committed entry.png to the output location.

make.fun program/v1 entry (Python 3.13, standard library only, no network):
the repository ships the finished image as entry.png next to this script,
and the grader runs this program twice in a fresh container with the
repository read-only and a writable output directory. Both runs must write
the same bytes, so this program simply copies the file, byte for byte.

Output: entry.png inside $MAKEFUN_OUTPUT_DIR when that environment
variable is set, otherwise /output/entry.png.
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SOURCE, dest)
    print(f"wrote {dest}")


if __name__ == "__main__":
    main()
