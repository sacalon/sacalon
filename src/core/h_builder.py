from .h_lexer import Lexer  # hascal lexer
from .h_parser import Parser  # hascal parser
from .h_compiler import Generator  # hascal to c++ compiler
from .h_error import HascalError  # hascal excpetion handling
from .h_help import *  # hascal compiler information
from .h_git import * # git related functions

from os.path import isfile,isdir,islink
from subprocess import DEVNULL, STDOUT, PIPE, check_call, Popen
import sys
import os
import requests
import json
import zipfile
import platform
import shutil

class HascalCompiler(object):
    def __init__(self, argv, BASE_DIR):
        self.BASE_DIR = BASE_DIR
        self.code = ""
        self.lexer = Lexer()
        self.parser = Parser()
        self.argv = argv
        # arguments checking
        if len(self.argv) > 1:
            if self.argv[1] == "help":
                # show help(full)
                help_all()
            elif self.argv[1] == "version":
                # show version
                print(f"Hascal {HASCAL_COMPILER_VERSION} --- {sys.platform}")
            # START : Package Manager
            elif self.argv[1] == "get":
                mod_name = self.argv[2]
                if len(self.argv) == 4 :
                    mod_name = self.argv[3]
                mod_name = mod_name.replace(".","/")
                if len(argv) < 3:
                    HascalError(
                        "You must give one package name to install\nusage :\n\thascal install <package_name>"
                    )

                print(f"Installing '{self.argv[2]}'...")
                if isdir(f"{self.BASE_DIR}/hlib/{self.argv[2]}"):
                    HascalError(f"Package '{self.argv[2]}' already installed, for update use 'hascal update'")
                
                # check if git is installed
                check_if_git_installed()

                # check if git repository exist
                check_if_git_repo_exist(self.argv[2])

                # clone repository
                clone_repo(self.argv[2], f"{self.BASE_DIR}/hlib/{mod_name}")
                
                print(f"Module '{self.argv[2]}' installed successfully!")
            
            elif self.argv[1] == "update":
                mod_name = self.argv[2]
                mod_name = mod_name.replace(".","/")
                if not isdir(f"{self.BASE_DIR}/hlib/{mod_name}"):
                    HascalError(f"Module '{mod_name}' is not installed, use 'hascal get' to install it")
                print(f"Updating '{mod_name}'...")

                
                # check if git is installed
                check_if_git_installed()

                # check if git repository exist
                check_if_git_repo_exist(self.argv[2])

                # update repository
                update_repo(f"{self.BASE_DIR}/hlib/{mod_name}")

                print(f"Module '{self.argv[2]}' updated successfully!")
            
            elif self.argv[1] == "list":
                print("List of installed packages :")
                for root, dirs, files in os.walk(f"{self.BASE_DIR}/hlib"):
                    for dir in dirs:
                        print(f" - {dir}")
                    for file in files:
                        if file.endswith(".has"):
                            print(f" - {file[:-4]}")
            elif len(self.argv) == 3 and self.argv[1] == "list" :
                print(f"list of all subpackages in '{self.argv[2]}' :")
                for root, dirs, files in os.walk(f"{self.BASE_DIR}/hlib/{self.argv[2]}"):
                    for dir in dirs:
                        print(f" - {dir}")
                    for file in files:
                        if file.endswith(".has"):
                            print(f" - {file[:-4]}")
            # END : Package Manager
            
            elif self.argv[1] == "--verbose":  # print ast
                if len(self.argv) == 3:
                    self.read_file(self.argv[2])
                    tokens = self.lexer.tokenize(self.code)
                    tree = self.parser.parse(tokens)
                    print(tree)
                else:
                    HascalError(
                        "You must give one file name to print ast\nusage :\n\thascal --verbose <file_name>"
                    )
            else:
                # check file extension
                if not self.argv[1].endswith(".has"):
                    # show file extension error
                    HascalError(f"The specified file is not a hascal(.has) file")
                else:
                    self.filename = self.argv[1]
                    self.read_file(self.argv[1])
                    self.compile()
        else:
            help_short()

    # hascal to c++ compiler function
    def compile(self):
        tmp0 = self.argv[1]
        outname = self.argv[2] if len(self.argv) > 2 else tmp0[:-4]
        ARGS = {
            "compiler": "g++",
            "optimize": "",
            "flags": ["-o", outname],
            "no_check_g++": 1,
            "ccfile": outname + ".cc",
            "c++_version": "c++17",
            "g++_out": False,
            "c++_code": False,
            "only_compile" : False,
            "no_std" : False
        }

        if os.path.isfile("config.json"):
            with open("config.json", "r") as f:
                config = json.loads(f.read())

                if "compiler" in config:
                    ARGS["compiler"] = config["compiler"]
                if "optimize" in config:
                    ARGS["optimize"] = config["optimize"]
                if "flags" in config:
                    ARGS["flags"] += config["flags"]
                if "g++_out" in config:
                    ARGS["g++_out"] = config["g++_out"]
                if "c++_code" in config:
                    ARGS["c++_code"] = config["c++_code"]
                if "no_std" in config:
                    ARGS["no_std"] = config["no_std"]
                if "only_compile" in config :
                    ARGS["only_compile"] = config["only_compile"]
                if ARGS["compiler"] != "g++" :
                    ARGS["no_check_gcc_g++"] = False
                
        
        tokens = self.lexer.tokenize(self.code)
        tree = self.parser.parse(tokens)

        generator = Generator(self.BASE_DIR,filename=self.filename,no_std=ARGS["no_std"])
        output = generator.generate(tree)

        for flag in generator.get_flags():
            if not flag in ARGS["flags"]:
                ARGS["flags"].append(flag)
        
        # write output c++ code in a file
        with open(outname + ".cc", "w") as fout:
            fout.write(output)
        
        # user may use other compiler instead of gcc\g++ for compiling hascal programs
        if ARGS["no_check_g++"] == True:
            # check if gcc installed
            try:
                check_call(["g++", "--version"], stdout=DEVNULL, stderr=STDOUT)
            except:
                HascalError("GCC/G++ is not installed")

        # check if c++ compiler installed
        try:
            check_call([ARGS["compiler"], "--version"], stdout=DEVNULL, stderr=STDOUT)
        except:
            HascalError("C++ compiler is not installed")

        # check if c++ compiler supports ARGS["c++_version"]
        compiler_process = Popen(
            [ARGS["compiler"], "-dumpversion"], stdout=PIPE, stderr=STDOUT
        )
        out, err = compiler_process.communicate()
        out = out.decode("utf-8")
        if int(out.split(".")[0]) < 8:
            HascalError("C++ compiler doesn't support c++17")

        if ARGS["only_compile"] == True :
            ARGS["flags"][1] += ".o"
            ARGS["flags"].append("-c")
        
        # compile to binary
        try:
            compargs = [
                ARGS["compiler"],
                f'-std={ARGS["c++_version"]}',
                ARGS["optimize"],
                ARGS["ccfile"],
            ] + ARGS["flags"]

            for i in range(len(compargs) - 1):
                if compargs[i] == "":
                    compargs.pop(i)

            if ARGS["g++_out"] == 1:
                check_call(compargs)
            else:
                check_call(compargs, stdout=DEVNULL, stderr=STDOUT)
        except:
            HascalError("Unknown error in compile file")

        if ARGS["c++_code"] == True:
            ...
        else:
            try:
                os.remove(outname + ".cc")
            except:
                ...

    def read_file(self, file_name):
        try:
            with open(file_name, encoding="utf-8") as fin:
                self.code = fin.read()
        except FileNotFoundError:
            HascalError(f"File '{file_name}' not found")