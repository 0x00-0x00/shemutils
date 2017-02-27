#!/usr/bin/env python3.6
# Test script made to test data shredding functions.
# -----------------------------------------------------

import os
import binascii
import random


def new_name():
    return binascii.hexlify(os.urandom(16)) + ".txt".encode()


def new_content():
    return os.urandom(random.randint(256, 4096))


def main():
    written = 0
    for _ in range(16):
        fname = new_name().decode()
        with open("files/{0}".format(fname), "wb") as f:
            f.write(new_content())
            written += 1

    print("[+] Written {0} test data files.".format(written))
    return 0


if __name__ == "__main__":
    main()

