from .h_lexer import Lexer # hascal lexer
from .h_parser import Parser # hascal parser
from .h_compiler import Generator,HLIB_BASE_DIR # hascal to d compiler
from .h_error import HascalError # hascal excpetion handling
from .h_help import * # hascal compiler information

from os.path import isfile 
from subprocess import DEVNULL, STDOUT, check_call, getoutput
import sys
import os
import requests
import json
import zipfile
import platform


def show_help(all=False):
    if all:
        help_all()
    else:
        help_short()
    
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
            if self.argv[1] == "help":
                # show help
                show_help(True)
                sys.exit()
            elif self.argv[1] == "version":
                # show version
                print(f"Hascal {HASCAL_COMPILER_VERSION} --- {sys.platform}")
            # START : Library Manager
            elif self.argv[1] in "install" :
                if len(argv) < 3 :
                    HascalError("You must give one library name to install\nusage :\n\thascal install <library_name>")
                print(f"Installing '{self.argv[2]}'...")
                if os.path.isfile(self.BASE_DIR+"/hlib/index.json"):
                    print("Update Libraries Index...")
                    index = get_index()
                    with open(self.BASE_DIR+"/hlib/index.json","w") as f:
                        f.write(json.dumps(index))
                    if not self.argv[2] in index :
                        HascalError(f"Library {self.argv[2]} not found")
                    # dowload zip file
                    r = requests.get(f"{BASE_URL}/{self.argv[2]}/{index[self.argv[2]]['zip']}")
                    # write zip file to disk
                    with open(self.BASE_DIR+"/hlib/tmp.zip","wb") as f :
                        f.write(r.content)
                    # extract downloaded zip file to hlib folder
                    with zipfile.ZipFile(self.BASE_DIR+"/hlib/tmp.zip", 'r') as zip_ref:
                        zip_ref.extractall(self.BASE_DIR+"/hlib/")
                    # remove downloaded zip file
                    os.remove(self.BASE_DIR+"/hlib/tmp.zip")
                    
                else :
                    print("Get Libraries Index")
                    index = get_index()
                    with open(self.BASE_DIR+"/hlib/index.json","w") as f:
                        f.write(json.dumps(index))
                    if not self.argv[2] in index :
                        HascalError(f"Library {self.argv[2]} not found")

                    # dowload zip file
                    r = requests.get(f"{BASE_URL}/{self.argv[2]}/{index[self.argv[2]]['zip']}")
                    # write zip file to disk
                    with open(self.BASE_DIR+"/hlib/tmp.zip","wb") as f :
                        f.write(r.content)
                    # extract downloaded zip file to hlib folder
                    with zipfile.ZipFile(self.BASE_DIR+"/hlib/tmp.zip", 'r') as zip_ref:
                        zip_ref.extractall(self.BASE_DIR+"/hlib/")
                    # remove downloaded zip file
                    os.remove(self.BASE_DIR+"/hlib/tmp.zip")
                print(f"'{self.argv[2]}' library installed successfully!")

            elif self.argv[1] == "uninstall" : # todo
                HascalError("Uninstalling library is not implemented in this version.")

            elif self.argv[1] == "update" :
                if len(argv) < 3 :
                    HascalError("You must give one library name to update\nusage :\n\thascal update <library_name>")
                if not os.path.isfile(self.BASE_DIR+"/hlib/index.json"):
                    HascalError("Library index file(index.json) not found in 'hlib' folder")
                print(f"Updating '{self.argv[2]}'...")
                if os.path.isfile(self.BASE_DIR+"/hlib/index.json"):
                    print("Update Libraries Index...")
                    index = get_index()
                    with open(self.BASE_DIR+"/hlib/index.json","w") as f:
                        f.write(json.dumps(index))
                    if not self.argv[2] in index :
                        HascalError(f"Library {self.argv[2]} is deleted from server, you have currently latest version.")
                    # dowload zip file
                    r = requests.get(f"{BASE_URL}/{self.argv[2]}/{index[self.argv[2]]['zip']}")
                    # write zip file to disk
                    with open(self.BASE_DIR+"/hlib/tmp.zip","wb") as f :
                        f.write(r.content)
                    # extract downloaded zip file to hlib folder
                    with zipfile.ZipFile(self.BASE_DIR+"/hlib/tmp.zip", 'r') as zip_ref:
                        zip_ref.extractall(self.BASE_DIR+"/hlib/")
                    # remove downloaded zip file
                    os.remove(self.BASE_DIR+"/hlib/tmp.zip")

                print(f"'{self.argv[2]}' library updated successfully!")
            elif self.argv[1] == "export" :
                if len(argv) < 3 :
                    HascalError("You must give one zip file name to export library(only name not extension)\nusage :\n\thascal export <zip_file_name>")
                current_dir = os.getcwd()
                zipf = zipfile.ZipFile(self.argv[2]+".zip", 'w', zipfile.ZIP_DEFLATED)
                zipdir(current_dir, zipf)
                zipf.close()
            # END : Library Manager
            elif self.argv[1] == "--verbose" : # print ast
                if len(self.argv) == 3 :
                    self.read_file(self.argv[2])
                    tokens = self.lexer.tokenize(self.code)
                    tree = self.parser.parse(tokens)
                    print(tree)
                else :
                    HascalError("You must give one file name to print ast\nusage :\n\thascal --verbose <file_name>")
            else :
                # check file extension
                if not self.argv[1].endswith(".has"):
                    # show file extension error 
                    HascalError(f"The specified file is not a hascal(.has) file")
                else :
                    self.read_file(self.argv[1])
                    self.compile()
        else:
            show_help()
            sys.exit()

    # hascal to c++ compiler function
    def compile(self):
        tokens = self.lexer.tokenize(self.code)
        tree = self.parser.parse(tokens)
        output = self.generator.generate(tree)
        HLIB_BASE_DIR = self.BASE_DIR+"\\hlib\\" if sys.platform == "win32" else self.BASE_DIR+"/hlib/"

        tmp0 = self.argv[1]
        outname = self.argv[2] if len(self.argv) > 2 else tmp0[:-4]

        # write output c++ code in a file
        with open(outname+".cc", 'w') as fout:
            fout.write(output)

        ARGS = {
            "compiler" : "g++",
            "optimize" : "",
            "flags" : ['-o',outname],
            "no_check_gcc_g++" : 1,
            "ccfile" : outname+".cc",
            "c++_version" : "c++17",
            "g++_out" : 0,
            "c++_code" : 0,
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
                if "no_check_gcc_g++" in config :
                    ARGS["no_check_gcc_g++"] = config["no_check_gcc_g++"]
                if "g++_out" in config :
                    ARGS["g++_out"] = config["g++_out"]

        # user may use other compiler instead of gcc\g++ for compiling hascal programs
        if ARGS["no_check_gcc_g++"] == 1 :
            # check if gcc installed
            try :
                check_call(['g++','--version'], stdout=DEVNULL, stderr=STDOUT)
            except :
                HascalError("GCC/G++ is not installed")   

        # check if c++ compiler installed
        try :
            check_call([ARGS["compiler"], '--version'], stdout=DEVNULL, stderr=STDOUT)
        except :
            HascalError("C++ compiler is not installed")
        
        # check if c++ compiler supports ARGS["c++_version"]
        try :
            if int(getoutput(f'{ARGS["compiler"]} -dumpversion').split(".")[0]) < 8:
                HascalError("C++ compiler doesn't support c++17")
            
        except :
            HascalError(f"C++ compiler is not support {ARGS['c++_version']}")
        
        # compile to binary
        try :
            compargs = [ARGS["compiler"],f'-std={ARGS["c++_version"]}',ARGS["optimize"],ARGS["ccfile"]] + ARGS["flags"]
            for i in range(len(compargs)-1):
                if compargs[i] == '' :
                    compargs.pop(i)

            if ARGS["g++_out"] == 1 :         
                check_call(compargs)
            else :
                check_call(compargs, stdout=DEVNULL, stderr=STDOUT)
        except :
            HascalError("Unknown error in compile file")

        if ARGS["c++_code"] == 1 :
            ...
        else :
            try :
                os.remove(outname+".cc")
            except :
                ...
    def read_file(self,file_name):
        try:
            with open(file_name,encoding="utf-8") as fin:
                self.code = fin.read()  
        except FileNotFoundError :
            HascalError(f"File '{file_name}' not found")
        

BASE_URL = "https://raw.githubusercontent.com/hascal/libs/main"

def get_index():
    r = requests.get(f"{BASE_URL}/index.json")
    if r :
        return r.json()
    else :
        HascalError("Cannot download libraries index")
    
def zipdir(path, ziph):
    length = len(path)
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        folder = root[length:] # path without "parent"
        for file in files:
            ziph.write(os.path.join(root, file), os.path.join(folder, file))