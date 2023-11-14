#!/usr/bin/env python3

import sys
import os
from core.sa_builder import SacalonCompiler
import pathlib

def main():
    BASE_DIR = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    SacalonCompiler(sys.argv, BASE_DIR)

if __name__ == "__main__":
    try : main()
    except KeyboardInterrupt : ...
