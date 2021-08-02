# h_builder.py
#
# The Hascal Programming Language
# Copyright 2019-2021 Hascal Development Team,
# all rights reserved.

from .h_lexer import Lexer # hascal lexer
from .h_parser import Parser # hascal parser
from .h_compiler import Generator # hascal to d compiler
from .h_error import HascalException # hascal excpetion handling
from .h_help import * # hascal compiler information

from .colorama import init,Fore # colorama library for coloring console output

from os.path import isfile 
from subprocess import DEVNULL, STDOUT, check_call
import sys
import os

class HascalCompiler(object):
    def __init__(self,argv):
        init() # init colorama

        self.code = ""
        self.lexer = Lexer()
        self.parser = Parser()
        self.generator = Generator()
        self.argv = argv
        
        # arguments checking
        if len(self.argv) > 1 :
            if self.argv[1] == "-h" or self.argv[1] == "--help":
                # show help
                output_message = [f"Hascal Compiler {HASCAL_COMPILER_VERSION} {sys.platform}",
                                    "Copyright (c) 2019-2021 Hascal Development Team,",
                                    "All rights reserved.",
                                    "\nEnter following command for compile a Hascal program :",
                                    "hascal <inputfile.has> [output file name]",
                                    "other commands:",
                                    "\t--help,-h : show help",
                                    "\t--version,-v : show version"]
                for msg in output_message:
                    print(msg)
                sys.exit()
            elif self.argv[1] == "-v" or self.argv[1] == "--version":
                # show version
                print(f"Hascal {HASCAL_COMPILER_VERSION} {sys.platform}")
            else :
                # check file extension
                if not self.argv[1].endswith(".has"):
                    # show file extension error 
                    HascalException(f"Error : The specified file is not a hascal(.has) file")
                else :
                    try:
                        with open(argv[1]) as fin:
                            self.code = fin.read()
                        self.compile()
                    except FileNotFoundError :
                        HascalException(f"Error : File '{argv[1]}' not found")
        else:
            output_message = [f"Hascal Compiler {HASCAL_COMPILER_VERSION} {sys.platform}",
                                "Copyright (c) 2019-2021 Hascal Development Team,",
                                "All rights reserved.",
                                "\nEnter following command for compile a Hascal program :",
                                "hascal <inputfile.has>",
                                "other commands:",
                                "\t--help,-h : show help",
                                "\t--version,-v : show version"]
            for msg in output_message:
                print(msg)
            sys.exit()

    # hascal to d compiler function
    def compile(self):
        tokens = self.lexer.tokenize(self.code)
        tree = self.parser.parse(tokens)
        output = self.generator.generate(tree)

        tmp0 = self.argv[1]
        excutable_outname = self.argv[2] if len(self.argv) > 2 else tmp0[:-4]
        outname = "out.d"

        # write output js code in a file
        with open(outname, 'w') as fout:
            fout.write(output)

        # set output excutable file
        tmp0 = self.argv[1]
        tmp = '-of=' + excutable_outname

        # compile with dmd compiler
        try :
            check_call(['dmd',"out.d", tmp],stdout=DEVNULL,stderr=STDOUT)
            # os.system('dmd '+'out.d '+tmp)
            os.remove("out.d")
        except :
            output_messages = [
                "Error : Your code have error(s)",
                "Check these items :",
                "\t1-incompatible types",
                "\t2-functions arguements and types and length of arguments",
                "\t3-modify consts",
                "\tand more..."
                f"\nif you could not troubleshooting your code , create an issue in hascal github repository({HASCAL_GITHUB_REPO}) ,we helps you "
            ]
            for msg in output_messages:
                print(Fore.RED+msg)