from .sa_lexer import Lexer  # sacalon lexer
from .sa_parser import Parser  # sacalon parser
from .sa_compiler import Generator  # sacalon to c++ compiler
from .sa_error import SacalonError  # sacalon excpetion handling
from .sa_help import *  # sacalon compiler information
from .sa_git import * # git related functions

from os.path import isfile,isdir
from pathlib import Path
from subprocess import DEVNULL, STDOUT, PIPE, check_call, Popen, CalledProcessError
import sys
import os
import json

class SacalonCompiler(object):
    def __init__(self, argv, BASE_DIR):
        self.BASE_DIR = BASE_DIR
        self.code = ""
        self.filename = ""
        self.lexer = Lexer()
        self.parser = Parser()
        self.argv = argv

        # arguments checking
        if len(self.argv) > 1:
            if self.argv[1] == "help":
                # show full help
                help_all()
            
            elif self.argv[1] == "version":
                # show version
                print(f"Sacalon {SACALON_COMPILER_VERSION} --- {sys.platform}")
            
            # START : Package Manager

            elif self.argv[1] == "get":
                if len(argv) < 3:
                    SacalonError(
                        "You must give one package name to install\nusage :\n\tsacalon get <package_name>"
                    )
                
                mod_name = self.argv[2]
                if len(self.argv) == 4 :
                    mod_name = self.argv[3]
                mod_name = mod_name.replace(".","/")

                print(f"Installing '{self.argv[2]}'...")
                if isdir(f"{self.BASE_DIR}/salivan/{self.argv[2]}"):
                    SacalonError(f"Package '{self.argv[2]}' already installed, for update use 'sacalon update {mod_name}'")
                
                # check if git is installed
                check_if_git_installed()

                # check if git repository exist
                check_if_git_repo_exist(self.argv[2])

                # clone repository
                clone_repo(self.argv[2], f"{self.BASE_DIR}/salivan/{mod_name}")
                
                print(f"Module '{self.argv[2]}' installed successfully!")
            
            elif self.argv[1] == "update":
                if len(argv) < 3:
                    SacalonError(
                        "You must give one package name to update\nusage :\n\tsacalon update <package_name>"
                    )
                
                mod_name = self.argv[2]
                mod_name = mod_name.replace(".","/")

                if not isdir(f"{self.BASE_DIR}/salivan/{mod_name}"):
                    SacalonError(f"Module '{mod_name}' is not installed, use 'sacalon get' to install it")
                print(f"Updating '{mod_name}'...")

                
                # check if git is installed
                check_if_git_installed()

                # check if git repository exist
                check_if_git_repo_exist(self.argv[2])

                # update repository
                update_repo(f"{self.BASE_DIR}/salivan/{mod_name}")

                print(f"Module '{self.argv[2]}' updated successfully!")
            
            elif self.argv[1] == "list":
                print("List of installed packages :")
                for root, dirs, files in os.walk(f"{self.BASE_DIR}/salivan"):
                    for dir in dirs:
                        print(f" - {dir}")
                    for file in files:
                        if file.endswith(".sa"):
                            print(f" - {file[:-4]}")
            
            elif len(self.argv) == 3 and self.argv[1] == "list" :
                print(f"list of all subpackages in '{self.argv[2]}' :")
                for root, dirs, files in os.walk(f"{self.BASE_DIR}/salivan/{self.argv[2]}"):
                    for dir in dirs:
                        print(f" - {dir}")
                    for file in files:
                        if file.endswith(".sa"):
                            print(f" - {file[:-4]}")
            
            # END : Package Manager

            # START : Project Manager

            # create new project
            elif self.argv[1] == "init" :
                with open("config.json","w",encoding="utf-8") as f :
                    f.write(json.dumps({
                        "filename" : "src/app.sa",
                        "outfile" : "build/app",
                    }))

                if not isdir("src") :
                    os.mkdir("src")
                with open("src/app.sa","w",encoding="utf-8") as f :
                    f.write("function main():int{\n\tprint(\"Hello World!\")\n\treturn 0\n}")

                with open(".gitignore","w",encoding="utf-8") as f :
                    ignores = ["/build",
                        "**.exe", "**.out",
                        "**.dll","**.o", "**.a"
                    ]
                    for ignore in ignores :
                        f.write(ignore)
            
            # build project
            elif self.argv[1] == "build" :
                self.compile(from_config=True)
            
            # build and run project
            elif self.argv[1] == "run" :
                if len(self.argv) == 3 :
                    self.filename = self.argv[2]
                    self.read_file(self.argv[2])
                    self.compile(run=True)
                else :
                    self.compile(from_config=True,run=True)
            
            # END : Project Manager

            # print ast
            elif self.argv[1] == "verbose":  
                if len(self.argv) == 3:
                    self.read_file(self.argv[2])
                    tokens = self.lexer.tokenize(self.code)
                    tree = self.parser.parse(tokens)
                    print(tree)
                else:
                    SacalonError(
                        "You must give one file name to print ast\nusage :\n\tsacalon verbose <file_name>"
                    )
            
            else:
                # check file extension
                if not self.argv[1].endswith(".sa"):
                    # show file extension error
                    SacalonError(f"The specified file is not a sacalon(.sa) file")
                else:
                    self.filename = self.argv[1]
                    self.read_file(self.argv[1])
                    self.compile()
        else:
            help_short()

    # sacalon to c++ compiler function
    def compile(self,from_config=False,run=False):
        """
        Compile Sacalon code to C++ code

        Args :
            from_config(bool,optional) : build code from project's config
            run(bool,optional) : run code after build
        """

        # Sacalon always builds code from a builtin config
        ARGS = {
            "filename" : self.filename, # main filename that contains entry function(main)
            "compiler": "g++", # compiler name
            "optimize": "", # optimize level
            "flags": [], # flags to pass to c++ compiler
            "ccfile": self.filename[:-4]+".cc", # output c++ code
            "c++_version": "c++17", # c++ standard version>=c++17
            "compiler_output": False, # compiler output
            "c++_code": False, # generate c++ code, if it is false, generated c++ code will delete after compiling
            "only_compile" : False, # only compile, not link
            "no_std" : False, # not link runtime library to code
            "outfile" : self.filename[:-4],
            "null_safety" : True,
        }

        # read config file
        if os.path.isfile("config.json"):
            with open("config.json", "r",encoding="utf-8") as f:
                config = json.loads(f.read())

                if "filename" in config :
                    # check if the filename field points to a Sacalon file
                    if "filename" != self.filename :
                        if not config["filename"].endswith(".sa"):
                            SacalonError(f"The specified file is not a sacalon(.sa) file")
                        self.filename = config["filename"]
                        self.read_file(self.filename)
                    ARGS["ccfile"] = self.filename[:-4]+".cc"
                elif from_config :
                    SacalonError("When you use `build` command, your config file should have `filename` field.")
                
                if "compiler" in config:
                    ARGS["compiler"] = config["compiler"]
                
                if "optimize" in config:
                    ARGS["optimize"] = config["optimize"]
                
                if "flags" in config:
                    if from_config :
                        filename = Path(self.filename)
                        ARGS["flags"] = ["-o","build/"+filename.name[:-4]] + config["flags"]
                    else :
                        ARGS["flags"] += config["flags"]
                if "compiler_output" in config:
                    ARGS["compiler_output"] = config["compiler_output"]
                
                if "c++_code" in config:
                    ARGS["c++_code"] = config["c++_code"]
                
                if "no_std" in config:
                    ARGS["no_std"] = config["no_std"]
                
                if "only_compile" in config :
                    ARGS["only_compile"] = config["only_compile"]
                if "outfile" in config :
                    ARGS["outfile"] = config["outfile"]
                if "null_safety" in config:
                    ARGS["null_safety"] = config["null_safety"]

        # tokenize input code
        tokens = self.lexer.tokenize(self.code)

        # parse tokens
        tree = self.parser.parse(tokens)

        # generate c++ code from ast
        generator = Generator(self.BASE_DIR,filename=self.filename,no_std=ARGS["no_std"])
        output = generator.generate(tree)

        # get flags from generator(some times, when you using a libray, 
        # it needs some extra flags for compiling such as `http` library)
        for flag in generator.get_flags():
            if not flag in ARGS["flags"]:
                ARGS["flags"].append(flag)
        
        # write output c++ code in a file
        with open(self.filename[:-4]+".cc", "w",encoding="utf-8") as fout:
            fout.write(output)

        # check if c++ compiler installed
        try:
            check_call([ARGS["compiler"], "--version"], stdout=DEVNULL, stderr=STDOUT)
        except:
            SacalonError("C++ compiler is not installed")

        # check if c++ compiler supports ARGS["c++_version"]
        out = ""
        if ARGS["compiler"] in ["g++","gcc","clang++","clang","avr-gcc","avr-g++",
                                "x86_64-elf-gcc","x86_64-elf-g++"] :
            compiler_process = Popen(
                [ARGS["compiler"], "-dumpversion"], stdout=PIPE, stderr=STDOUT
            )
            out, _ = compiler_process.communicate()
        else :
            compier = ARGS["compiler"]
            SacalonError(f"'{compier}' is not supported yet, use g++ or clang++")
        
        # TODO : Support more compilers(msvc,icc,apple clang,...)
        out = out.decode("utf-8")

        # check c++ compiler version that supports c++17 or greater
        if (ARGS["compiler"] in ["clang","clang++"] and int(out.split(".")[0]) < 10)  \
            or (ARGS["compiler"] in ["gcc","g++"] and int(out.split(".")[0]) < 7):
                SacalonError("C++ compiler doesn't support c++17")

        if ARGS["only_compile"] == True :
            ARGS["flags"][1] += ".o"
            ARGS["flags"].append("-c")
        
        # create outfile dir
        if not isdir(Path(ARGS["outfile"]).parent) :
            os.makedirs(Path(ARGS["outfile"]).parent)
        # compile to binary
        try:
            compargs = [
                ARGS["compiler"],
                f'-std={ARGS["c++_version"]}',
                ARGS["optimize"],
                ARGS["ccfile"],
            ] + ARGS["flags"] + ["-o",ARGS["outfile"]]

            for i in range(len(compargs) - 1):
                if compargs[i] == "":
                    compargs.pop(i)

            if ARGS["compiler_output"] == 1:
                check_call(compargs)
            else:
                check_call(compargs, stdout=DEVNULL, stderr=STDOUT)
        except:
            SacalonError("Unknown error in compile file")


        if ARGS["c++_code"] == True:
            ...
        else:
            try: os.remove(self.filename[:-4]+".cc")
            except:...
        
        # run generated excutable
        if run :
            filename = ARGS["outfile"] if from_config else self.filename[:-4]

            if sys.platform.startswith("win"):
                if isfile(filename+".exe"):
                    try : check_call([filename+".exe"])
                    except CalledProcessError as e :...
                else :
                    SacalonError(f"Excutable file not found, make sure `only_compile` in your config file is'nt `true`")
            else :
                if isfile("./" + filename):
                    try :check_call(["./" +filename])
                    except CalledProcessError as e :...
                elif isfile("./" + filename + ".out"):
                    try : check_call(["./"+ + filename + ".out"])
                    except CalledProcessError as e :...
                else :
                    SacalonError(f"Excutable file not found, make sure `only_compile` in your config file is'nt `true`")



    def read_file(self, file_name):
        try:
            with open(file_name, encoding="utf-8") as fin:
                self.code = fin.read()
        except FileNotFoundError:
            SacalonError(f"File '{file_name}' not found")