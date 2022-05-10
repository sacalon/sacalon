#!/usr/bin/env python3

# The Hascal Application
#
# The Hascal Programming Language
# Copyright 2019-2022 Hascal Development Team,
# all rights reserved.

import sys
from core.h_builder import HascalCompiler
import pathlib

def main():
    BASE_DIR = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    HascalCompiler(sys.argv, BASE_DIR)

if __name__ == "__main__":
    main()
