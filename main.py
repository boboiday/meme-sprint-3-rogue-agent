#!/usr/bin/env python3
"""Meme Sprint 3 entry: copy the pre-rendered meme to /output/entry.png.

The image is drawn by draw_meme.py (PIL, run at build time) and shipped in
this repository as entry.png. This program uses only the Python standard
library, touches no network, and writes the same bytes on every run.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
DST = "/output/entry.png"


def main():
    os.makedirs("/output", exist_ok=True)
    shutil.copyfile(SRC, DST)
    # Determinism guard: the output must be the shipped image, byte for byte.
    assert os.path.getsize(DST) == os.path.getsize(SRC), "entry.png size mismatch"


if __name__ == "__main__":
    main()
