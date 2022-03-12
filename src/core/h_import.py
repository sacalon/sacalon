from .h_lexer import Lexer
from .h_parser import Parser
from .h_error import HascalError, HascalWarning
from sys import platform
from os.path import isfile

def use(gen_class,path,BASE_DIR,filename=None):
    result = {}
    name = '.'.join(name for name in path)

    if platform.startswith('win'):
            final_path = str(BASE_DIR+"\\hlib\\")
            final_path_local = ""

            for x in path:
                final_path += x + "\\"
                final_path_local += x + "\\"

            final_path = final_path[:-1] + ".has"
            final_path_local = final_path_local[:-1] + ".has"

            if isfile(final_path) :
                with open(final_path,'r') as f :
                    parser = Parser()
                    tree = parser.parse(Lexer().tokenize(f.read()))
                                                
                    generator = gen_class(BASE_DIR)
                    output_cpp = generator.generate(tree,True)

                    result['generator'] = generator
                    result['output_cpp'] = output_cpp
                    return result
            elif isfile(final_path_local):
                with open(final_path_local,'r') as f :
                    parser = Parser()
                    tree = parser.parse(Lexer().tokenize(f.read()))
                                                
                    generator = gen_class(BASE_DIR)
                    output_cpp = generator.generate(tree,True)

                    result['generator'] = generator
                    result['output_cpp'] = output_cpp
                    return result
            else :
                HascalError(f"cannot found '{name}' library. Are you missing a library ?")
    else :
            final_path = str(BASE_DIR+"/hlib/")
            final_path_local = ""

            for x in path:
                final_path += x + "/"
                final_path_local += x + "/"

            final_path = final_path[:-1] + ".has"
            final_path_local = final_path_local[:-1] + ".has"

            if isfile(final_path) :
                with open(final_path,'r') as f :
                    parser = Parser()
                    tree = parser.parse(Lexer().tokenize(f.read()))
                                                
                    generator = gen_class(BASE_DIR)
                    output_cpp = generator.generate(tree,True)

                    result['generator'] = generator
                    result['output_cpp'] = output_cpp
                    return result
            elif isfile(final_path_local):
                with open(final_path_local,'r') as f :
                    parser = Parser()
                    tree = parser.parse(Lexer().tokenize(f.read()))
                                                
                    generator = gen_class(BASE_DIR)
                    output_cpp = generator.generate(tree,True)

                    result['generator'] = generator
                    result['output_cpp'] = output_cpp
                    return result
            else :
                HascalError(f"cannot found '{name}' library. Are you missing a library ?")