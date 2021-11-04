# The Hascal Compiler
#
# The Hascal Programming Language
# Copyright 2019-2022 Hascal Development Team,
# all rights reserved.

from .h_error import HascalException
from .h_lexer import Lexer
from .h_parser import Parser
import sys

class Generator(object):
      def __init__(self,BASE_DIR):
            self.BASE_DIR = BASE_DIR
            self.src_includes = ""
            self.src_pre_main = ""
            #init standard types
            self.types = ['int','float','bool','char','string','auto','File','JSONValue']

            # init built-in variables and init variables list
            self.vars = ['argv']
            self.stdvars = ['argv']

            # init functions list
            self.funcs = ['print',
                         'to_string']

            # list of imported libraries
            self.imported = []
      def generate(self, tree,use=False):
            if self.test(tree):
                  result = self.walk(tree)
                  if use :
                        return f"\n{self.src_pre_main}\n"
                  else :
                        runtime = open(self.BASE_DIR+"/hlib/d/std.d").read()
                        runtime_h = open(self.BASE_DIR+"/hlib/d/std.h").read()
                        return f"{runtime_h}\n{runtime}\n{self.src_includes}\n{self.src_pre_main}\n{result}\n"


      def test(self, tree):
            def has_node(t, node_name):
                  for item in t[1:]:
                        if isinstance(item, tuple) and len(item) > 0:
                              if item[0] == node_name: return True
                              if has_node(item, node_name): return True
                  return False
            try :
                  for statement in tree[1:]:
                        if has_node(statement, 'function'):
                              HascalException("Error : You can't declere functions under another block")
                              return False
                  return True
            except :
                  sys.exit(1)
      
      def exists(self,name):
            if name in self.funcs:
                  return True
            elif name in self.types :
                  return True
            elif name in self.vars :
                  return True
            return False
      def add_to_output(self,d_code,dh_code):
            self.src_includes += '\n' + dh_code + '\n'
            self.src_pre_main += '\n' + d_code + '\n'

      def walk(self, node):
            # {
            #     <statements>
            # }
            if node[0] == 'block':
                  result = ""
                  for statement in node[1:]:
                        result += self.walk(statement) or ""
                  return result
            if node[0] == 'in_block':
                  result = ""
                  for statement in node[1:]:
                        result += self.walk(statement) or ""
                  return result
            if node[0] == 'block_struct':
                  current_vars = self.vars
                  self.vars = [] + self.stdvars
                  result = ""
                  for statement in node[1:]:
                        result += self.walk(statement) or ""
                  self.vars = current_vars
                  return result
            #-------------------------------------
            # statement declares :
            
            # var <name> : <return_type> ;
            if node[0] == 'declare' and node[1] == "no_equal":
                  if node[3] in self.vars :
                        HascalException(f"Error : '{node[3]}' exists ,cannot redefine it")
                        sys.exit(1)
                  elif node[3] in self.types :
                        HascalException(f"Error : '{node[3]}' defined as a type ,cannot redefine it as a variable")
                        sys.exit(1)
                  else:
                        if node[2] in self.types :
                              self.vars.append(node[3])
                              self.src_pre_main += "%s %s ;\n" % (node[2],node[3])
                        else :
                              HascalException(f"Error : type '{node[2]}' not defined")
                              sys.exit(1)
            # var <name> : <return_type> = <expr> ;
            if node[0] == 'declare' and node[1] == "equal2":
                  if node[3] in self.vars :
                        HascalException(f"Error : '{node[3]}' exists ,cannot redefine it")
                        sys.exit(1)
                  elif node[3] in self.types :
                        HascalException(f"Error : '{node[3]}' defined as a type ,cannot redefine it as a variable")
                        sys.exit(1)
                  else:
                        if node[2] in self.types :
                              self.vars.append(node[3])
                              self.src_pre_main += "%s %s = %s;\n" % (node[2],node[3],self.walk(node[4]))
                        else :
                              HascalException(f"Error : type '{node[2]}' not defined")
                              sys.exit(1)

            # var <name> = <expr> ;
            if node[0] == 'declare' and node[1] == "equal1":
                  if node[3] in self.vars :
                        HascalException(f"Error : '{node[3]}' exists ,cannot redefine it")
                        sys.exit(1)
                  elif node[3] in self.types :
                        HascalException(f"Error : '{node[3]}' defined as a type ,cannot redefine it as a variable")
                        sys.exit(1)
                  else:
                        if node[2] in self.types :
                              self.vars.append(node[3])
                              self.src_pre_main += "auto %s = %s ;\n" % (node[3],self.walk(node[4]))
                        else :
                              HascalException(f"Error : type '{node[2]}' not defined")
                              sys.exit(1)
            
            # var <name> : [<return_type>] ;
            if node[0] == 'declare_array' and node[1] == "no_equal":
                  if node[3] in self.vars :
                        HascalException(f"Error : '{node[3]}' exists ,cannot redefine it")
                        sys.exit(1)
                  elif node[3] in self.types :
                        HascalException(f"Error : '{node[3]}' defined as a type ,cannot redefine it as a variable")
                        sys.exit(1)
                  else:
                        if node[2] in self.types :
                              self.vars.append(node[3])
                              self.src_pre_main += "%s[] %s ;\n" % (node[2],node[3])
                        else :
                              HascalException(f"Error : type '{node[2]}' not defined")
                              sys.exit(1)
            
            # var <name> = <expr> ;
            if node[0] == 'declare_array' and node[1] == "equal1":
                  if node[3] in self.vars :
                        HascalException(f"Error : '{node[3]}' exists ,cannot redefine it")
                        sys.exit(1)
                  elif node[3] in self.types :
                        HascalException(f"Error : '{node[3]}' defined as a type ,cannot redefine it as a variable")
                        sys.exit(1)
                  else:
                        if node[2] in self.types :
                              self.vars.append(node[3])
                              self.src_pre_main += "auto %s = %s ;\n" % (node[3],self.walk(node[4]))
                        else :
                              HascalException(f"Error : type '{node[2]}' not defined")
                              sys.exit(1)

            # var <name> : [<return_type>] = <expr>;
            if node[0] == 'declare_array' and node[1] == "equal2":
                  if node[3] in self.vars :
                        HascalException(f"Error : '{node[3]}' exists ,cannot redefine it")
                        sys.exit(1)
                  elif node[3] in self.types :
                        HascalException(f"Error : '{node[3]}' defined as a type ,cannot redefine it as a variable")
                        sys.exit(1)
                  else:
                        if node[2] in self.types :
                              self.vars.append(node[3])
                              self.src_pre_main += "%s[] %s = %s ;\n" % (node[2],node[3],self.walk(node[4]))
                        else :
                              HascalException(f"Error : type '{node[2]}' not defined")
                              sys.exit(1)
                              
            # const <name> = <expr> ;
            if node[0] == 'declare' and node[1] == "const":
                  if node[2] in self.vars :
                        HascalException(f"Error : '{node[2]}' exists ,cannot redefine it")
                        sys.exit(1)
                  elif node[2] in self.types :
                        HascalException(f"Error : '{node[2]}' defined as a type ,cannot redefine it as a variable")
                        sys.exit(1)
                  else:
                        self.vars.append(node[2])
                        self.src_pre_main += "const %s = %s ;\n" % (node[2],self.walk(node[3]))
            
            # const <name> : <return_type> = <expr> ;
            if node[0] == 'declare' and node[1] == "const_type":
                  if node[3] in self.vars :
                        HascalException(f"Error : '{node[3]}' exists ,cannot redefine it")
                        sys.exit(1)
                  elif node[3] in self.types :
                        HascalException(f"Error : '{node[3]}' defined as a type ,cannot redefine it as a variable")
                        sys.exit(1)
                  else:
                        self.vars.append(node[3])
                        self.src_pre_main += "const %s %s = %s ;\n" % (node[2],node[3],self.walk(node[4]))
            #-------------------------------------
            # in_statement declares :
            
            # in : var <name> : <return_type> ;
            if node[0] == 'in_declare' and node[1] == "no_equal":
                  if node[3] in self.vars :
                        HascalException(f"Error : '{node[3]}' exists ,cannot redefine it")
                        sys.exit(1)
                  elif node[3] in self.types :
                        HascalException(f"Error : '{node[3]}' defined as a type ,cannot redefine it as a variable")
                        sys.exit(1)
                  else:
                        if node[2] in self.types :
                              self.vars.append(node[3])
                              return "%s %s ;\n" % (node[2],node[3])
                        else :
                              HascalException(f"Error : type '{node[2]}' not defined")
                              sys.exit(1)
            # in : var <name> : <return_type> = <expr> ;
            if node[0] == 'in_declare' and node[1] == "equal2":
                  if node[3] in self.vars :
                        HascalException(f"Error : '{node[3]}' exists ,cannot redefine it")
                        sys.exit(1)
                  elif node[3] in self.types :
                        HascalException(f"Error : '{node[3]}' defined as a type ,cannot redefine it as a variable")
                        sys.exit(1)
                  else:
                        if node[2] in self.types :
                              self.vars.append(node[3])
                              return "%s %s = %s;\n" % (node[2],node[3],self.walk(node[4]))
                        else :
                              HascalException(f"Error : type '{node[2]}' not defined")
                              sys.exit(1)

            # in : var <name> = <expr> ;
            if node[0] == 'in_declare' and node[1] == "equal1":
                  if node[3] in self.vars :
                        HascalException(f"Error : '{node[3]}' exists ,cannot redefine it")
                        sys.exit(1)
                  elif node[3] in self.types :
                        HascalException(f"Error : '{node[3]}' defined as a type ,cannot redefine it as a variable")
                        sys.exit(1)
                  else:
                        if node[2] in self.types :
                              self.vars.append(node[3])
                              return "auto %s = %s ;\n" % (node[3],self.walk(node[4]))
                        else :
                              HascalException(f"Error : type '{node[2]}' not defined")
                              sys.exit(1)
            
            # in : var <name> : [<return_type>] ;
            if node[0] == 'in_declare_array' and node[1] == "no_equal":
                  if node[3] in self.vars :
                        HascalException(f"Error : '{node[3]}' exists ,cannot redefine it")
                        sys.exit(1)
                  elif node[3] in self.types :
                        HascalException(f"Error : '{node[3]}' defined as a type ,cannot redefine it as a variable")
                        sys.exit(1)
                  else:
                        if node[2] in self.types :
                              self.vars.append(node[3])
                              return "%s[] %s ;\n" % (node[2],node[3])
                        else :
                              HascalException(f"Error : type '{node[2]}' not defined")
                              sys.exit(1)
            
            # in : var <name> = <expr> ;
            if node[0] == 'in_declare_array' and node[1] == "equal1":
                  if node[3] in self.vars :
                        HascalException(f"Error : '{node[3]}' exists ,cannot redefine it")
                        sys.exit(1)
                  elif node[3] in self.types :
                        HascalException(f"Error : '{node[3]}' defined as a type ,cannot redefine it as a variable")
                        sys.exit(1)
                  else:
                        if node[2] in self.types :
                              self.vars.append(node[3])
                              return "auto %s = %s ;\n" % (node[3],self.walk(node[4]))
                        else :
                              HascalException(f"Error : type '{node[2]}' not defined")
                              sys.exit(1)

            # in : var <name> : [<return_type>] = <expr>;
            if node[0] == 'in_declare_array' and node[1] == "equal2":
                  if node[3] in self.vars :
                        HascalException(f"Error : '{node[3]}' exists ,cannot redefine it")
                        sys.exit(1)
                  elif node[3] in self.types :
                        HascalException(f"Error : '{node[3]}' defined as a type ,cannot redefine it as a variable")
                        sys.exit(1)
                  else:
                        if node[2] in self.types :
                              self.vars.append(node[3])
                              return "%s[] %s = %s ;\n" % (node[2],node[3],self.walk(node[4]))
                        else :
                              HascalException(f"Error : type '{node[2]}' not defined")
                              sys.exit(1)
                              
            # in : const <name> = <expr> ;
            if node[0] == 'in_declare' and node[1] == "const":
                  if node[2] in self.vars :
                        HascalException(f"Error : '{node[2]}' exists ,cannot redefine it")
                        sys.exit(1)
                  elif node[2] in self.types :
                        HascalException(f"Error : '{node[2]}' defined as a type ,cannot redefine it as a variable")
                        sys.exit(1)
                  else:
                        self.vars.append(node[2])
                        return "const %s = %s ;\n" % (node[2],self.walk(node[3]))
            # in : const <name> : <return_type> = <expr> ;
            if node[0] == 'in_declare' and node[1] == "const_type":
                  if node[3] in self.vars :
                        HascalException(f"Error : '{node[3]}' exists ,cannot redefine it")
                        sys.exit(1)
                  elif node[3] in self.types :
                        HascalException(f"Error : '{node[3]}' defined as a type ,cannot redefine it as a variable")
                        sys.exit(1)
                  else:
                        self.vars.append(node[3])
                        return "const %s %s = %s ;\n" % (node[2],node[3],self.walk(node[4]))
            #-------------------------------------
            # <name> = <expr> ;         
            if node[0] == 'assign':
                  if len(node[1]) == 1:
                        name = node[1][0]
                        if name in self.vars:
                               return "%s = %s;\n" % (name, self.walk(node[2]))
                        elif name in self.types:
                              HascalException(f"Error : '{name}'is a type ,cannot change it")
                              sys.exit(1)
                        else :
                              HascalException(f"Error : variable '{name}' not defined")
                              sys.exit(1) 
                  else :
                        name = node[1][0]
                        if name in self.vars :     
                              all_names = '.'.join(arg for arg in node[1])
                              
                              return "%s = %s;\n" % (all_names, self.walk(node[2]))
                        elif name in self.types:
                              HascalException(f"Error : '{name}'is a type ,cannot change it")
                              sys.exit(1) 
                        else :
                              HascalException(f"Error : variable '{name}' not defined")
                              sys.exit(1) 
                  sys.exit(1)

            # <name>[<expr>] = <expr>;
            if node[0] == 'assign_var_index':
                  if len(node[1]) == 1:
                        name = node[1][0]
                        if name in self.vars:
                               return "%s[%s] = %s;\n" % (name,self.walk(node[2]), self.walk(node[3]))
                        elif name in self.types:
                              HascalException(f"Error : '{name}'is a type ,cannot change it")
                              sys.exit(1)
                        else :
                              HascalException(f"Error : variable '{name}' not defined")
                              sys.exit(1) 
                  else :
                        name = node[1][0]
                        if name in self.vars :     
                              all_names = '.'.join(arg for arg in node[1])
                              
                              return "%s[%s] = %s;\n" % (all_names,self.walk(node[2]), self.walk(node[3]))
                        elif name in self.types:
                              HascalException(f"Error : '{name}'is a type ,cannot change it")
                              sys.exit(1) 
                        else :
                              HascalException(f"Error : variable '{name}' not defined")
                              sys.exit(1) 
                  sys.exit(1)
            #-----------------------------------------
            # return <expr> ;
            if node[0] == 'return':
                  return "return %s;\n" % self.walk(node[1])
            #-----------------------------------------
            # break  ;
            if node[0] == 'break':
                  return "break;\n"
            
            # continue  ;
            if node[0] == 'continue':
                  return "continue;\n"
            #-----------------------------------------
            # use <lib_name> ;
            if node[0] == 'use':
                  if sys.platform.startswith('win32'):
                        if node[1] in self.imported :
                              ...
                        else :
                              name = '.'.join(name for name in node[1])
                              if name.startswith("d.") :
                                    path = node[1]
                                    final_path = str(self.BASE_DIR+"\\hlib\\")

                                    ends_of_path = path[-1]
                                    for x in path[:-1]:
                                          final_path += x + "\\"
                                    final_path_h = final_path + ends_of_path + ".h"
                                    final_path += ends_of_path + ".d"
                                    try:
                                          with open(final_path, 'r') as fd:
                                                d_code = fd.read()
                                                with open(final_path_h,'r') as fh :
                                                      dh_code = fh.read()
                                                      self.imported.append(name)
                                                      self.add_to_output(d_code,dh_code)
                                    except FileNotFoundError:
                                          HascalException(f"Error : cannot found '{name}' library. Are you missing a library ?")
                                          sys.exit(1)
                              else :
                                    path = node[1]
                                    final_path = str(self.BASE_DIR+"\\hlib\\")

                                    ends_of_path = path[-1]
                                    for x in path[:-1]:
                                          final_path += x + "\\"
                                    final_path += ends_of_path + ".has"

                                    try:
                                          with open(final_path, 'r') as f:
                                                parser = Parser()
                                                tree = parser.parse(Lexer().tokenize(f.read()))
                                                generator = Generator()
                                                output_d = generator.generate(tree,True)

                                                self.imported.append(name)
                                                self.imported += generator.imported
                                                self.add_to_output(output_d,generator.src_includes)
                                                self.funcs += generator.funcs
                                                self.types += generator.types
                                    except FileNotFoundError:
                                          HascalException(f"Error : cannot found '{name}' library. Are you missing a library ?")
                                          sys.exit(1)

                  else :
                        if node[1] in self.imported :
                              ...
                        else :
                              name = '.'.join(name for name in node[1])
                              if name.startswith("d.") :
                                    path = node[1]
                                    final_path = str(self.BASE_DIR+"/hlib/")

                                    ends_of_path = path[-1]
                                    for x in path[:-1]:
                                          final_path += x + "/"
                                    final_path_h = final_path + ends_of_path + ".h"
                                    final_path += ends_of_path + ".d"
                                    try:
                                          with open(final_path, 'r') as fd:
                                                d_code = fd.read()
                                                with open(final_path_h,'r') as fh :
                                                      dh_code = fh.read()
                                                      self.imported.append(name)
                                                      self.add_to_output(d_code,dh_code)
                                    except FileNotFoundError:
                                          HascalException(f"Error : cannot found '{name}' library. Are you missing a library ?")
                                          sys.exit(1)
                              else :
                                    path = node[1]
                                    final_path = str(self.BASE_DIR+"/hlib/")

                                    ends_of_path = path[-1]
                                    for x in path[:-1]:
                                          final_path += x + "/"
                                    final_path += ends_of_path + ".has"

                                    try:
                                          with open(final_path, 'r') as f:
                                                parser = Parser()
                                                tree = parser.parse(Lexer().tokenize(f.read()))
                                                generator = Generator()
                                                output_d = generator.generate(tree,True)

                                                self.imported.append(name)
                                                self.imported += generator.imported
                                                self.add_to_output(output_d,generator.src_includes)
                                                self.funcs += generator.funcs
                                                self.types += generator.types
                                    except FileNotFoundError:
                                          HascalException(f"Error : cannot found '{name}' library. Are you missing a library ?")
                                          sys.exit(1)
            
            # local use <lib_name> ;
            if node[0] == 'use_local':
                  if sys.platform.startswith('win32'):
                        if node[1] in self.imported :
                              ...
                        else :
                              name = '.'.join(name for name in node[1])
                              if name.startswith("d."):
                                    path = name.split('.')
                                    final_path = ""

                                    ends_of_path = path[-1]
                                    for x in path[:-1]:
                                          final_path += x + "\\"
                                    final_path_h = final_path + ends_of_path + ".h"
                                    final_path += ends_of_path + ".d"

                                    try:
                                          with open(final_path, 'r') as fd:
                                                d_code = fd.read()
                                                with open(final_path_h,'r') as fh :
                                                      dh_code = fh.read()
                                                      self.imported.append(name)
                                                      self.add_to_output(d_code,dh_code)
                                    except FileNotFoundError:
                                          HascalException(f"Error : cannot found '{name}' library. Are you missing a library ?")

                              else :
                                    tmp = '.'.join(name for name in node[1])
                                    path = tmp.split('.')
                                    final_path = ""

                                    ends_of_path = path[-1]
                                    for x in path[:-1]:
                                          final_path += x + "\\"
                                    final_path += ends_of_path + ".has"

                                    try:
                                          with open(final_path, 'r') as f:
                                                parser = Parser()
                                                tree = parser.parse(Lexer().tokenize(f.read()))
                                                generator = Generator()
                                                output_d = generator.generate(tree,True)

                                                self.imported.append(name)
                                                self.imported += generator.imported
                                                self.add_to_output(output_d, generator.src_includes)
                                                self.funcs += generator.funcs
                                    except FileNotFoundError:
                                          HascalException(f"Error : cannot found '{name}' library. Are you missing a library ?")
                              
                  elif sys.platform.startswith('linux'):
                        name = '.'.join(name for name in node[1])
                        if name.startswith("d."):
                              path = name.split('.')
                              final_path = ""

                              ends_of_path = path[-1]
                              for x in path[:-1]:
                                    final_path += x + "/"
                              final_path_h = final_path + ends_of_path + ".h"
                              final_path += ends_of_path + ".d"

                              try:
                                    with open(final_path, 'r') as fd:
                                          d_code = fd.read()
                                          with open(final_path_h,'r') as fh :
                                                dh_code = fh.read()
                                                self.imported.append(name)
                                                self.add_to_output(d_code,dh_code)
                              except FileNotFoundError:
                                    HascalException(f"Error : cannot found '{name}' library. Are you missing a library ?")

                        else :
                              tmp = '.'.join(name for name in node[1])
                              path = tmp.split('.')
                              final_path = ""

                              ends_of_path = path[-1]
                              for x in path[:-1]:
                                    final_path += x + "/"
                              final_path += ends_of_path + ".has"

                              try:
                                    with open(final_path, 'r') as f:
                                          parser = Parser()
                                          tree = parser.parse(Lexer().tokenize(f.read()))
                                          generator = Generator()
                                          output_d = generator.generate(tree,True)

                                          self.imported.append(name)
                                          self.imported += generator.imported
                                          self.add_to_output(output_d, generator.src_includes)
                                          self.funcs += generator.funcs
                              except FileNotFoundError:
                                    HascalException(f"Error : cannot found '{name}' library. Are you missing a library ?")
            #-----------------------------------------
            # function <name> {
            #     <block>
            # }
            # or :
            # function <name> : <return_type> {
            #     <block>
            # }

            # function <name>() {
            #     <block>
            # }
            # or :
            # function <name>() : <return_type> {
            #     <block>
            # }

            # function <name>(<args>) {
            #     <block>
            # }
            # or :
            # function <name>(<args>) : <return_type> {
            #     <block>
            # }
            if node[0] == 'function':
                  current_vars = self.vars
                  self.funcs.append(node[2])

                  params = node[3].split(',')
                  param_vars = []
                  if len(params) != 1:
                        for p in params:
                              p2 = p.split(' ')
                              param_vars.append(p2[1])
                        for p in param_vars:
                              self.vars.append(p)
                  elif len(params) == 0 : 
                        pass
                  else :
                        if params[0] == '' or params[0] == None :
                              pass
                        else :
                              params2 = params[0].split(' ')
                              self.vars.append(params2[1])
                  res = self.walk(node[4])

                  self.src_pre_main += "%s %s(%s) {\n%s\n}\n" % (node[1],node[2], node[3],res) 
                  self.vars = current_vars
            #-------------------------------------
            if node[0] == "inline_function" :
                  self.funcs.append(node[2])
            #-------------------------------------
            # struct <name> {
            #     <struct_declare>
            # }
            if node[0] == 'struct':
                  name = node[1]
                  body = self.walk(node[2])
                  self.types.append(name)
                  self.src_pre_main += "struct %s{\n%s\n}\n" % (name,body)
            #-------------------------------------
            # enum <name> {
            #     <enum_names>
            # }
            if node[0] == 'enum':
                  name = node[1]
                  names = node[2]
                  self.types.append(name)
                  self.src_pre_main += "enum %s{\n%s\n}\n" % (name,names)
            #-------------------------------------
            # if <condition> {
            #     <block>
            # }   

            # or : 

            # if <condition> {
            #     <block>
            # }else {
            #     <block>
            # }

            # or :

            # if <condition> {
            #     <block>
            # }else if <condition> {
            #     <block>
            # }
            if node[0] == 'if':
                  cond = self.walk(node[1])
                  body = self.walk(node[2])
                  return "if(%s){\n%s\n}\n" % (cond,body)
            if node[0] == 'if_else':
                  cond = self.walk(node[1])
                  body = self.walk(node[2])
                  body2 = self.walk(node[3])
                  return "if(%s){\n%s\n}else {\n%s\n}\n" % (cond,body,body2)
            if node[0] == 'if_else2':
                  cond = self.walk(node[1])
                  body = self.walk(node[2])
                  return "if(%s){\n%s\n}else %s\n" % (cond,body,self.walk(node[3]))
            #------------------------------------
            # for <name> to <expr> {
            #     <block>
            # }
            if node[0] == 'for':      
                  name = node[1]
                  expr0 = self.walk(node[2])
                  expr1 = self.walk(node[3])
                  body = self.walk(node[4])
                  return "for(%s=%s;%s<=%s;%s++){\n%s\n}\n" % (name,expr0,name,expr1,name,body)
            
            # for <name> downto <expr> {
            #     <block>
            # }
            if node[0] == 'for_down':      
                  name = node[1]
                  expr0 = self.walk(node[2])
                  expr1 = self.walk(node[3])
                  body = self.walk(node[4])
                  return "for(%s=%s;%s>=%s;%s--){\n%s\n}\n" % (name,expr0,name,expr1,name,body)
            #--------------------------------------
            # while <condition> {
            #     <block>
            # }
            if node[0] == 'while':      
                  cond = self.walk(node[1])
                  body = self.walk(node[2])
                  return "while(%s){\n%s\n}\n" % (cond,body)
            #---------------------------------------
            # <expr> ;                    
            if node[0] == 'expr':
                  return "%s;\n" % self.walk(node[1])
            #---------------------------------------
            # <expr>(<params>);
            if node[0] == 'call':
                  if self.exists(node[1]):
                        if node[1] == "print":
                              return "writeln(%s)" % (', '.join(self.walk(arg) for arg in node[2]))
                        else :
                              return "%s(%s)" % (node[1], ', '.join(self.walk(arg) for arg in node[2]))
                  else :
                        HascalException(f"Error : function '{node[1]}' not defined")
                        sys.exit(1)
            # --------------operators-----------------
            if node[0] == 'add':
                  return "%s + %s" % (self.walk(node[1]), self.walk(node[2]))
            if node[0] == 'add_cont':
                  return "%s ~ %s" % (self.walk(node[1]), self.walk(node[2]))
            if node[0] == 'sub':
                  return "%s - %s" % (self.walk(node[1]), self.walk(node[2]))
            if node[0] == 'mul':
                  return "%s * %s" % (self.walk(node[1]), self.walk(node[2]))
            if node[0] == 'div':
                  return "%s / %s" % (self.walk(node[1]), self.walk(node[2]))
            if node[0] == 'pow':
                  return "%s ^ %s" % (self.walk(node[1]), self.walk(node[2]))
            if node[0] == 'paren_expr':
                  return "(%s)" % (self.walk(node[1]))
            if node[0] == 'cond':
                  return "%s" % (self.walk(node[1]))

            if node[0] == 'not':
                  return "!%s" % (self.walk(node[1]))

            if node[0] == 'and':
                  return "%s && %s" % (self.walk(node[1]),self.walk(node[2]))

            if node[0] == 'or':
                  return "%s || %s" % (self.walk(node[1]),self.walk(node[2]))
            # --------------end of operators-----------------  

            # ---------------conditions---------------------
            # <expr> == <expr>
            if node[0] == 'equals':
                  return "%s == %s" % (self.walk(node[1]), self.walk(node[2]))

            # <expr> != <expr>
            if node[0] == 'not_equals':
                  return "%s != %s" % (self.walk(node[1]), self.walk(node[2]))

            # <expr> >= <expr>
            if node[0] == 'greater_equals':
                  return "%s >= %s" % (self.walk(node[1]), self.walk(node[2]))

            # <expr> <= <expr>
            if node[0] == 'less_equals':
                  return "%s <= %s" % (self.walk(node[1]), self.walk(node[2]))
            
            # <expr> > <expr>
            if node[0] == 'greater':
                  return "%s > %s" % (self.walk(node[1]), self.walk(node[2]))

            # <expr> < <expr>
            if node[0] == 'less':
                  return "%s < %s" % (self.walk(node[1]), self.walk(node[2]))

            # not <expr>
            if node[0] == 'not_cond':
                  return "!%s" % (self.walk(node[1]))

            # true / false
            if node[0] == 'bool_cond':
                  return "%s" % (node[1])
            # ---------------end of conditions---------------------     
            # <name>
            if node[0] == 'var':
                  if len(node[1]) == 1:
                        name = node[1][0]
                        if self.exists(name):
                               return "%s" % (name)
                        else :
                              HascalException(f"Error : variable '{name}' not defined")
                              sys.exit(1) 
                  else :
                        name = node[1][0]
                        if self.exists(name) :     
                              all_names = '.'.join(arg for arg in node[1])
                              return "%s" % (all_names)
                        else :
                              HascalException(f"Error : variable '{name}' not defined")
                              sys.exit(1) 
                  sys.exit(1)
            
            # <name>[<expr>]
            if node[0] == 'var_index':
                  if len(node[1]) == 1:
                        name = node[1][0]
                        if name in self.vars:
                               return "%s[%s]" % (name,self.walk(node[2]))

                        else :
                              HascalException(f"Error : variable '{name}' not defined")
                              sys.exit(1) 
                  else :
                        name = node[1][0]
                        if name in self.vars :     
                              all_names = '.'.join(arg for arg in node[1])
                              return "%s[%s]" % (all_names,self.walk(node[2]))
                        else :
                              HascalException(f"Error : variable '{name}' not defined")
                              sys.exit(1) 
                  sys.exit(1)
            #-------------------------------------------
            # <expr> , <expr>
            if node[0] == 'exprs':
                  return '%s,%s' % (self.walk(node[1]),self.walk(node[2]))
            # [<expr>]
            if node[0] == 'list':
                  return '[%s]' % (self.walk(node[1]))
            #-------------------------------------------
            # <expr>.<name>
            if node[0] == '.':
                  return '%s.%s' % (self.walk(node[1]),node[2])
            # <expr>.<name>
            if node[0] == '.2':
                  return '%s.%s[%s]' % (self.walk(node[1]),node[2],self.walk(node[3]))
            #--------------------------------------------
            if node[0] == 'string':
                  return '"%s".dup' % node[1]
            if node[0] == 'bool':
                  return '%s' % node[1]
            if node[0] == 'float':
                  return '%s' % node[1]
            if node[0] == 'char':
                  return '\'%s\'' % node[1]
            if node[0] == 'number':
                  return '%s' % node[1]
            #---------------------------------------------