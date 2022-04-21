#!/usr/bin/env python3

# The Hascal Application
#
# The Hascal Programming Language
# Copyright 2019-2022 Hascal Development Team,
# all rights reserved.

from sys import argv
from core.h_builder import HascalCompiler
import pathlib


def main():
    BASE_DIR = str(pathlib.Path(__file__).parent.resolve())
    HascalCompiler(argv, BASE_DIR)


if __name__ == "__main__":
    main()
