# The Hascal Compiler CLI
#
# The Hascal Programming Language
# Copyright 2019-2022 Hascal Development Team,
# all rights reserved.

from .h_lexer import Lexer # hascal lexer
from .h_parser import Parser # hascal parser
from .h_compiler import Generator # hascal to d compiler
from .h_error import HascalException # hascal excpetion handling
from .h_help import * # hascal compiler information


from os.path import isfile 
from subprocess import DEVNULL, STDOUT, check_call
import sys
import os

class HascalCompiler(object):
    def __init__(self,argv,BASE_DIR):
        self.BASE_DIR = BASE_DIR
        self.code = ""
        self.lexer = Lexer()
        self.parser = Parser()
        self.generator = Generator(self.BASE_DIR)
        self.argv = argv
        # arguments checking
        if len(self.argv) > 1 :
            if self.argv[1] == "-h" or self.argv[1] == "--help":
                # show help
                output_message = [f"Hascal Compiler {HASCAL_COMPILER_VERSION} {sys.platform}",
                                    "Copyright (c) 2019-2022 Hascal Development Team,",
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
                print(f"Hascal {HASCAL_COMPILER_VERSION} --- {sys.platform}")
            else :
                # check file extension
                if not self.argv[1].endswith(".has"):
                    # show file extension error 
                    HascalException(f"The specified file is not a hascal(.has) file")
                else :
                    try:
                        with open(argv[1]) as fin:
                            self.code = fin.read()
                        self.compile()
                    except FileNotFoundError :
                        HascalException(f"File '{argv[1]}' not found")
        else:
            output_message = [f"Hascal Compiler {HASCAL_COMPILER_VERSION} {sys.platform}",
                                "Copyright (c) 2019-2022 Hascal Development Team,",
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
        outname = self.argv[2] if len(self.argv) > 2 else tmp0[:-4]

        # write output js code in a file
        with open(outname+".d", 'w') as fout:
            fout.write(output)

        # compile with dmd compiler
        try :
            check_call(['dmd', outname, '-O', '-mcpu=native'], stdout=DEVNULL, stderr=STDOUT)
            # uncomment it for development(and comment top line)
            # os.system('dmd '+ outname)
        except :
            HascalException("unknown error in compile file")

        try :
            os.remove(outname+".d")
            os.remove(outname+".obj")
        except :
            ...