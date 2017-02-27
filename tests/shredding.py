#!/bin/bash
import os
from shemutils.shred import Shredder

TARGET_EXT = ".txt"

shredder = Shredder()
for root, dircd, files in os.walk("files/"):
    for f in files:
        base, ext = os.path.splitext(f)
        if ext != TARGET_EXT:
            continue
        abspath = os.path.join(root, f)
        shredder.shred(abspath, remove=True, v=True)
