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
import requests
import json

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
            if self.argv[1] in ["-h","--help"]:
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
            elif self.argv[1] in ["-v","--version"]:
                # show version
                print(f"Hascal {HASCAL_COMPILER_VERSION} --- {sys.platform}")
            
            # START : Library Manager
            elif self.argv[1] == "install" :
                if len(argv) < 3 :
                    HascalException("You must give one library name to install\nusage :\n\thascal install <library_name>")
                print(f"Installing '{self.argv[2]}'...")
                if os.path.isfile(self.BASE_DIR+"/hlib/index.json"):
                    print("Update Libraries Index...")
                    index = get_index()
                    with open(self.BASE_DIR+"/hlib/index.json","w") as f:
                        f.write(json.dumps(index))
                    if not self.argv[2] in index :
                        HascalException(f"Library {self.argv[2]} not found")
                    # dowload files
                    for file in index[self.argv[2]]["files"] :
                        r = requests.get(f"{BASE_URL}/{self.argv[2]}/{file}")
                        with open(self.BASE_DIR+"/hlib/"+file,'w',encoding='utf-8') as f :
                            f.write(str(r.content.decode("utf-8")))
                else :
                    print("Get Libraries Index")
                    index = get_index()
                    with open(self.BASE_DIR+"/hlib/index.json","w") as f:
                        f.write(json.dumps(index))
                    if not self.argv[2] in index :
                        HascalException(f"Library {self.argv[2]} not found")     
                    # dowload files
                    for file in index[self.argv[2]]["files"] :
                        r = requests.get(f"{BASE_URL}/{self.argv[2]}/{file}")
                        with open(self.BASE_DIR+"/hlib/"+file,'w',encoding='utf-8') as f :
                            f.write(str(r.content.decode("utf-8")))
                print(f"'{self.argv[2]}' library installed successfully!")

            elif self.argv[1] == "uninstall" :
                if len(argv) < 3 :
                    HascalException("You must give one library name to uninstall\nusage :\n\thascal uninstall <library_name>")

                if not os.path.isfile(self.BASE_DIR+"/hlib/index.json"):
                    HascalException("Library index file(index.json) not found in 'hlib' folder")
                print(f"Uninstalling '{self.argv[2]}'...")
                data = ""
                with open(self.BASE_DIR+"/hlib/index.json",'r',encoding='utf-8') as f :
                    data = f.read()
                index = json.loads(data)
                if not self.argv[2] in index :
                    HascalException(f"Library {self.argv[2]} not found")
                for file in index[self.argv[2]]["files"] :
                    os.remove(self.BASE_DIR+"/hlib/"+file)
                print(f"'{self.argv[2]}' library uninstalled successfully!")

            elif self.argv[1] == "update" :
                if len(argv) < 3 :
                    HascalException("You must give one library name to update\nusage :\n\thascal update <library_name>")
                if not os.path.isfile(self.BASE_DIR+"/hlib/index.json"):
                    HascalException("Library index file(index.json) not found in 'hlib' folder")
                print(f"Updating '{self.argv[2]}'...")
                if os.path.isfile(self.BASE_DIR+"/hlib/index.json"):
                    print("Update Libraries Index...")
                    index = get_index()
                    with open(self.BASE_DIR+"/hlib/index.json","w") as f:
                        f.write(json.dumps(index))
                    if not self.argv[2] in index :
                        HascalException(f"Library {self.argv[2]} is deleted from server, you have currently latest version.")
                    # dowload files
                    for file in index[self.argv[2]]["files"] :
                        r = requests.get(f"{BASE_URL}/{self.argv[2]}/{file}")
                        with open(self.BASE_DIR+"/hlib/"+file,'w',encoding='utf-8') as f :
                            f.write(str(r.content.decode("utf-8")))
                print(f"'{self.argv[2]}' library updated successfully!")
            # END : Library Manager
            else :
                # check file extension
                if not self.argv[1].endswith(".has"):
                    # show file extension error 
                    HascalException(f"The specified file is not a hascal(.has) file")
                else :
                    try:
                        with open(argv[1]) as fin:
                            self.code = fin.read()  
                    except FileNotFoundError :
                        HascalException(f"File '{argv[1]}' not found")
                    self.compile()
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

    # hascal to c++ compiler function
    def compile(self):
        tokens = self.lexer.tokenize(self.code)
        tree = self.parser.parse(tokens)
        output = self.generator.generate(tree)

        tmp0 = self.argv[1]
        outname = self.argv[2] if len(self.argv) > 2 else tmp0[:-4]

        # write output c++ code in a file
        with open(outname+".cc", 'w') as fout:
            fout.write(output)

        # check if gcc installed
        try :
            check_call(['g++','--version'], stdout=DEVNULL, stderr=STDOUT)
        except :
            HascalException("GCC/G++ is not installed")
            sys.exit(1)

        ARGS = {
            "compiler" : "g++",
            "optimize" : "-O3",
            "flags" : ['-o',outname],
            "ccfile" : outname+".cc",
        }
        for flag in self.generator.get_flags() :
            if not flag in ARGS["flags"]:
                ARGS["flags"].append(flag)

        if os.path.isfile("config.json"):
            with open("config.json","r") as f :
                config = json.loads(f.read())
                if "compiler" in config :
                    ARGS["compiler"] = config["compiler"]
                if "optimize" in config :
                    ARGS["optimize"] = config["optimize"]
                if "flags" in config :
                    ARGS["flags"] += config["flags"]
                          
        # compile to binary
        try :
            check_call([ARGS["compiler"],ARGS["optimize"],ARGS["ccfile"]] + ARGS["flags"], stdout=DEVNULL, stderr=STDOUT)
            # uncomment it for development(and comment top line)
            # os.system(ARGS["compiler"] +" " + ARGS["optimize"] + " " + ARGS["ccfile"] + " " +flags_str)
        except :
            HascalException("unknown error in compile file")

        try :
            os.remove(outname+".cc")
        except :
            ...

BASE_URL = "https://raw.githubusercontent.com/hascal/libs/main"

def get_index():
    r = requests.get(f"{BASE_URL}/index.json")
    if r :
        return r.json()
    else :
        HascalException("Cannot download libraries index")