#!/usr/bin/env python3

import sys
import os
from core.h_builder import HascalCompiler
import pathlib

def main():
    BASE_DIR = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    HascalCompiler(sys.argv, BASE_DIR)

if __name__ == "__main__":
    try : main()
    except KeyboardInterrupt : ...
