# The Hascal Compiler Error Manager
#
# The Hascal Programming Language
# Copyright 2019-2022 Hascal Development Team,
# all rights reserved.

# this module is written by @pranavbaburaj
import sys
import colorama
class HascalException():
    def __init__(self, exception_message):
        colorama.init()
        sys.stderr.write(colorama.Fore.RED+"Error : ")
        sys.stderr.write(colorama.Style.RESET_ALL)
        sys.stderr.write(exception_message)
        