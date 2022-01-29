from .h_error import HascalError
from .h_lexer import Lexer
from .h_parser import Parser
import sys
from os.path import isfile
from pathlib import Path

HLIB_BASE_DIR = str(Path(__file__).parents[1])

class Generator(object):
      LDFLAGS = []
      def __init__(self,BASE_DIR):
            self.BASE_DIR = BASE_DIR
            self.src_includes = ""
            self.src_pre_main = ""
            #init standard types
            self.types = {
                  'int' : Type('int',True,category='number'),
                  'int8' : Type('int8',True,category='number'),
                  'int16' : Type('int16',True,category='number'),
                  'int32' : Type('int32',True,category='number'),
                  'int64' : Type('int64',True,category='number'),
                  'uint' : Type('uint',True,category='number'),
                  'uint8' : Type('uint8',True,category='number'),
                  'uint16' : Type('uint16',True,category='number'),
                  'uint32' : Type('uint32',True,category='number'),
                  'uint64' : Type('uint64',True,category='number'),


                  'float' : Type('float',True,category='number'),
                  'double' : Type('double',True,category='number'),

                  'bool' : Type('bool',True,category='number'),
                  'char' : Type('char',True,category='number'),
                  'string' : Type('string',True),
                  'void' : Type('void',True),
            }

            self.vars = { } # global vars
            self.consts = { } # global consts

            # functions
            self.funcs = {
                  'print' : Function('print',{'...':'...'},'void'),
                  'ReadStr' : Function('ReadStr',{},self.types['string']),
                  'ReadInt' : Function('ReadInt',{},self.types['int']),
                  'ReadFloat' : Function('ReadFloat',{},self.types['float']),
                  'ReadChar' : Function('ReadChar',{},self.types['char']),
                  'ReadBool' : Function('ReadBool',{},self.types['bool']),

                  'format' : Function('format',{'...':'...'},self.types['string']),
                  'split' : Function('split',{'str':'string','sep':'string'},self.types['string']),
                  'exit' : Function('exit',{'exit_code':'int'},self.types['void']),
                  'panic' : Function('panic',{'err_msg':'string'},self.types['string']),
                  'error' : Function('error',{'errmsg':'string'},self.types['void']),

                  'to_int' : Function('to_int',{'...':'...'},self.types['int']),
                  'to_string' : Function('to_string',{'...':'...'},self.types['string']),
                  'to_bool' : Function('to_bool',{'...':'...'},self.types['bool']),
                  'to_char' : Function('to_char',{'...':'...'},self.types['char']),
                  'to_float' : Function('to_float',{'...':'...'},self.types['float']),

                  'len' : Function('len',{'s':'string'},self.types['int']),
                  'len' : Function('len',{'vec':'T'},self.types['int']),
                  'append' : Function('append',{'vec':'T','val':'T'},self.types['int']),
                  'regex' : Function('regex',{'regex_str':'string','str':'string'},self.types['bool']),

                  'sizeof' : Function('sizeof',{'T':'T'},self.types['int']),

            }

            # list of imported libraries
            self.imported = []

            self.params_list = []
      def generate(self, tree,use=False):
            _expr = self.walk(tree)
            result = ""
            for e in _expr :
                  result += e['expr']
            if use :
                  return f"\n{self.src_includes}\n{self.src_pre_main}\n{result}"
            else :
                  runtime = open(self.BASE_DIR+"/hlib/libcpp/std.cc").read()
                  runtime_h = open(self.BASE_DIR+"/hlib/libcpp/std.hpp").read()
                  return f"{runtime_h}\n{runtime}\n{self.src_includes}\n{self.src_pre_main}\n{result}\n"
      def get_flags(self):
            return self.LDFLAGS
      def exists(self,name):
            if name in self.funcs:
                  return True
            elif name in self.types :
                  return True
            elif name in self.vars :
                  return True
            if name in self.consts:
                  return True
            return False

      def add_to_output(self,cpp_code,hpp_code):
            self.src_includes += '\n' + hpp_code + '\n'
            self.src_pre_main += '\n' + cpp_code + '\n'

      def walk(self, node):
            # {
            #     <statements>
            # }
            if node[0] == 'block':
                  result = [ ] # list of exprs and statements
                  for statement in node[1:]:
                        result.append(self.walk(statement))
                  return result
            if node[0] == 'in_block':
                  result = [ ] # list of exprs and statements
                  for statement in node[1:]:
                        result.append(self.walk(statement))
                  return result
            if node[0] == 'block_struct':
                  current_vars = self.vars
                  self.vars = { }
                  result = [ ] # list of exprs and statements
                  for statement in node[1:]:
                        result.append(self.walk(statement))
                  self.vars = current_vars
                  return result
            #-------------------------------------
            # statement declares :
            
            # var <name> = <expr>
            if node[0] == 'declare' and node[1] == "no_type":
                  _name = node[2]
                  _expr = self.walk(node[3])
                  _type = _expr['type']
                  _line = node[4]

                  if _name in self.vars or _name in self.consts :
                        HascalError(f"'{_name}' exists, cannot redefine it:{_line}")
                  elif _name in self.types :
                        HascalError(f"'{_name}' defined as a type, cannot redefine it as a variable:{_line}")
                  else:
                        members = {}

                        if isinstance(_type,Struct) :
                              members = _type.members
                        self.vars[_name] = Var(_name,_type,members=members)
                        res = "auto %s = %s;\n" % (_name,_expr['expr'])
                        expr = {
                              'expr' : res,
                              'type' : _type,
                              'name' : _name,
                        }
                        return expr

            # var <name> : <return_type>
            if node[0] == 'declare' and node[1] == "no_equal":
                  _name = node[3]
                  _type = self.walk(node[2])
                  _line = node[4]

                  if _name in self.vars or _name in self.consts :
                        HascalError(f"'{_name}' exists ,cannot redefine it:{_line}")
                  elif _name in self.types :
                        HascalError(f"'{_name}' defined as a type ,cannot redefine it as a variable:{_line}")  
                  else:
                        members = {}
                        if isinstance(_type['type'],Struct) : members = _type['type'].members
                        self.vars[_name] = Var(_name,_type['type'],members=members)
                        res =  "%s %s ;\n" % (_type['expr'],_name)

                        expr = {
                              'expr' : res,
                              'type' : _type['type'],
                              'name' : _name,
                        }
                        return expr

            # var <name> : <return_type> = <expr>
            if node[0] == 'declare' and node[1] == "equal2":
                  _name = node[3]
                  _type = self.walk(node[2])
                  _expr = self.walk(node[4])
                  _line = node[5]
            
                  if _name in self.vars or _name in self.consts  :
                        HascalError(f"'{_name}' exists ,cannot redefine it:{_line}")
                  elif _name in self.types :
                        HascalError(f"'{_name}' defined as a type ,cannot redefine it as a variable:{_line}")
                  elif is_compatible_type(_expr['type'],_type['type']) == False :
                        HascalError(f"Mismatched type {_type} and {_expr['type']}:{_line}")
                  else:
                        members = {}
                        if isinstance(_type['type'],Struct) : members = _type['type'].members
                        self.vars[_name] = Var(_name,_type['type'],members=members)

                        expr = {
                              'expr' : "%s %s = %s;\n" % (_type['expr'],_name,_expr['expr']),
                              'type' : _type['type'],
                              'name' : _name,
                        }
                        return expr
                        
            # var <name> : [<return_type>]
            if node[0] == 'declare_array' and node[1] == "no_equal":
                  _name = node[3]
                  _type = self.walk(node[2])
                  _line = node[4]

                  if _name in self.vars or _name in self.consts :
                        HascalError(f"'{_name}' exists ,cannot redefine it:{_line}")   
                  elif _name in self.types :
                        HascalError(f"'{_name}' defined as a type ,cannot redefine it as a variable:{_line}")   
   
                  else:
                        self.vars[_name] = Var(_name,Array(_type['type']),is_array=True)
                        expr = {
                              'expr' : "std::vector<%s> %s;\n" % (_type['expr'],_name),
                              'type' : Array(_type['type']),
                              'name' : _name,
                        }
                        return expr

            # var <name> : [<return_type>] = <expr>
            if node[0] == 'declare_array' and node[1] == "equal2":
                  _name = node[3]
                  _type = self.walk(node[2])
                  _expr = self.walk(node[4])
                  _line = node[5]

                  if _name in self.vars or _name in self.consts :
                        HascalError(f"'{_name}' exists ,cannot redefine it:{_line}")
                  elif _name in self.types :
                        HascalError(f"'{_name}' defined as a type ,cannot redefine it as a variable:{_line}")
                  elif is_compatible_type(_expr['type'],Array(_type['type'])) == False :
                        HascalError(f"Mismatched type {Array(_type['type'])} and {_expr['type']}:{_line}")    
                  else:
                        self.vars[_name] = Var(_name,Array(_type['type']),is_array=True)

                        expr = {
                              'expr' : "std::vector<%s> %s = %s ;\n" % (_type['expr'],_name,_expr['expr']),
                              'type' : Array(_type['type']),
                              'name' : _name,
                        }
                        return expr
                              
            # const <name> : <return_type> = <expr>
            if node[0] == 'declare' and node[1] == "const":
                  _name = node[3]
                  _type = self.walk(node[2])['expr']
                  _expr = self.walk(node[4])
                  _line = node[5]

                  if _name in self.vars or _name in self.consts :
                        HascalError(f"'{_name}' exists ,cannot redefine it:{_line}")
                  elif _name in self.types :
                        HascalError(f"'{_name}' defined as a type ,cannot redefine it as a constant:{_line}")
                  elif str(_type) != str(_expr['type']) :
                        HascalError(f"Mismatched type {_type} and {_expr['type']}:{_line}")  
                  elif not _type in self.types :
                        HascalError(f"Type '{_type}' not defined:{_line}")
                  else:
                        self.consts[_name] = Const(_name,self.types[_type])
                        expr = {
                              'expr' : "const %s %s = %s ;\n" % (_type,_name,_expr['expr']),
                              'type' : self.types[_type],
                              'name' : _name,
                        }
                        return expr

            # var <name> : *<return_type>
            if node[0] == 'declare_ptr' and node[1] == "no_equal":
                  _name = node[3]
                  _type = self.walk(node[2])
                  _line = node[4]
                  if _name in self.vars or _name in self.consts :
                        HascalError(f"'{_name}' exists ,cannot redefine it:{_line}")
                  elif _name in self.types :
                        HascalError(f"'{_name}' defined as a type ,cannot redefine it as a variable:{_line}")  
                  else:
                        members = {}
                        if isinstance(_type['type'],Struct)  : members = _type['type'].members
                        self.vars[_name] = Var(_name,_type['type'],members=members)
                        res =  "%s %s ;\n" % (_type['expr'],_name)

                        expr = {
                              'expr' : res,
                              'type' : _type['type'],
                              'name' : _name,
                        }
                        return expr

            # var <name> : *<return_type> = <expr>
            if node[0] == 'declare_ptr' and node[1] == "equal2":
                  _name = node[3]
                  _type = self.walk(node[2])
                  _expr = self.walk(node[4])
                  _line = node[5]
            
                  if _name in self.vars or _name in self.consts  :
                        HascalError(f"'{_name}' exists ,cannot redefine it:{_line}")
                  elif _name in self.types :
                        HascalError(f"'{_name}' defined as a type ,cannot redefine it as a variable:{_line}")
                  elif str(_type['type']) != str(_expr['type']) :
                        HascalError(f"Mismatched type {_type['type']} and {_expr['type']}:{_line}")
                  else:
                        members = {}
                        if isinstance(_type['type'],Struct)  : members = _type['type'].members
                        self.vars[_name] = Var(_name,_type['type'],members=members)

                        expr = {
                              'expr' : "%s %s = %s;\n" % (_type['type'],_name,_expr['expr']),
                              'type' : _type['type'],
                              'name' : _name,
                        }
                        return expr
            
            # const <name> = <expr>
            if node[0] == 'declare' and node[1] == "const":
                  _name = node[2]
                  _expr = self.walk(node[3])
                  _type = _expr['type']
                  _line = node[4]

                  if _name in self.vars or _name in self.consts :
                        HascalError(f"'{_name}' exists, cannot redefine it:{_line}")
                  elif _name in self.types :
                        HascalError(f"'{_name}' defined as a type, cannot redefine it as a constant:{_line}")   
                  else:
                        self.consts[_name] = Const(_name,self.types[_type])

                        expr = {
                              'expr' : "const auto %s = %s ;\n" % (_name,_expr['expr']),
                              'type' : self.types[_type],
                              'name' : _name,
                        }
                        return expr
            #-------------------------------------
            if node[0] == 'cuse':
                  _c_code = node[1]
                  return {
                        'expr' : _c_code+"\n",
                        'type' : '',
                        'cuse' : True,
                  }

            # cuse <lib_name>
            if node[0] == 'cinclude':
                  if node[1] in self.imported :
                        ...
                  if sys.platform.startswith('win'):
                        name = '.'.join(name for name in node[1])
                        path = node[1]
                        final_path = str(self.BASE_DIR+"\\hlib\\")

                        ends_of_path = path[-1]
                        for x in path[:-1]:
                              final_path += x + "\\"
                        final_path_ld = final_path + ends_of_path + ".ld"
                        # final_path_wld = final_path + ends_of_path + ".wld"
                        final_path_h = final_path + ends_of_path + ".hpp"
                        final_path += ends_of_path + ".cc"
                        try:
                              with open(final_path, 'r') as fd:
                                    cpp_code = fd.read()
                                    with open(final_path_h,'r') as fh :
                                          hpp_code = fh.read()
                                          self.imported.append(name)
                                          self.add_to_output(cpp_code,hpp_code)
                        except FileNotFoundError:
                              HascalError(f"cannot found '{name}' library. Are you missing a library ?")
                        # if isfile(final_path_wld):
                        #       with open(final_path_ld) as f:
                        #             ld = f.read().split(',')
                        #             self.LDFLAGS += ld  
                        if isfile(final_path_ld):
                              with open(final_path_ld) as f:
                                    ld = list(f.read().split(','))
                                    for i in ld :
                                          self.LDFLAGS.append(i)                                          
                  else :
                        name = '.'.join(name for name in node[1])
                        path = node[1]
                        final_path = str(self.BASE_DIR+"/hlib/")

                        ends_of_path = path[-1]
                        for x in path[:-1]:
                              final_path += x + "/"
                        final_path_ld = final_path + ends_of_path + ".ld"
                        # final_path_wld = final_path + ends_of_path + ".wld"
                        final_path_h = final_path + ends_of_path + ".hpp"
                        final_path += ends_of_path + ".cc"
                        try:
                              with open(final_path, 'r') as fd:
                                    cpp_code = fd.read()
                                    with open(final_path_h,'r') as fh :
                                          hpp_code = fh.read()
                                          self.imported.append(name)
                                          self.add_to_output(cpp_code,hpp_code)
                        except FileNotFoundError:
                              HascalError(f"cannot found '{name}' library. Are you missing a library ?")
                        # if isfile(final_path_wld):
                        #       with open(final_path_ld) as f:
                        #             ld = f.read().split(',')
                        #             self.LDFLAGS += ld  
                        if isfile(final_path_ld):
                              with open(final_path_ld) as f:
                                    ld = list(f.read().split(','))
                                    for i in ld :
                                          self.LDFLAGS.append(i)   

                  return {'expr':'','type':''}
            
            if node[0] == 'cinclude_local':
                  if node[1] in self.imported :
                        ...
                  if sys.platform.startswith('win32'):
                        name = '.'.join(name for name in node[1])
                        path = name.split('.')
                        final_path = ""

                        ends_of_path = path[-1]
                        for x in path[:-1]:
                              final_path += x + "\\"
                        final_path_ld = final_path + ends_of_path + ".ld"
                        final_path_h = final_path + ends_of_path + ".hpp"
                        final_path += ends_of_path + ".cc"

                        try:
                              with open(final_path, 'r') as fd:
                                    cpp_code = fd.read()
                                    with open(final_path_h,'r') as fh :
                                          hpp_code = fh.read()
                                          self.imported.append(name)
                                          self.add_to_output(cpp_code,hpp_code)
                        except FileNotFoundError:
                              HascalError(f"cannot found '{name}' library. Are you missing a library ?")
                        if isfile(final_path_ld):
                              with open(final_path_ld) as f:
                                    ld = f.read().split(',')
                                    self.LDFLAGS += ld  
                              
                  else :
                        name = '.'.join(name for name in node[1])
                        path = name.split('.')
                        final_path = ""

                        ends_of_path = path[-1]
                        for x in path[:-1]:
                              final_path += x + "\\"
                        final_path_ld = final_path + ends_of_path + ".ld"
                        final_path_h = final_path + ends_of_path + ".hpp"
                        final_path += ends_of_path + ".cc"

                        try:
                              with open(final_path, 'r') as fd:
                                    cpp_code = fd.read()
                                    with open(final_path_h,'r') as fh :
                                          hpp_code = fh.read()
                                          self.imported.append(name)
                                          self.add_to_output(cpp_code,hpp_code)
                        except FileNotFoundError:
                              HascalError(f"cannot found '{name}' library. Are you missing a library ?")
                        if isfile(final_path_ld):
                              with open(final_path_ld) as f:
                                    ld = f.read().split(',')
                                    self.LDFLAGS += ld  

                  return {'expr':'','type':''}
            #-------------------------------------
            # <name> = <expr>   
            if node[0] == 'assign':
                  _name = self.walk(node[1])
                  _expr = self.walk(node[2])
                  _line = node[3]

                  if is_compatible_type(_name['type'],_expr['type']) == False:
                        HascalError(f"Mismatched type '{_name['type']}' and '{_expr['type']}':{_line}") 
                  
                  expr = {
                        'expr' : '%s = %s;' % (_name['expr'],_expr['expr']),
                        'type' : _name['type']
                  }
                  return expr

            # <name>[<expr>] = <expr>;
            if node[0] == 'assign_var_index':
                  _name = self.walk(node[1])
                  _index = self.walk(node[2])
                  _expr = self.walk(node[3])
                  _line = node[4]

                  if not isinstance(_name['type'],Array) :
                        HascalError(f"'{_name['type']}' is not subscriptable:{_line}")

                  if is_compatible_type(_name['type'].type_obj,_expr['type']) == False:
                        HascalError(f"Mismatched type '{_name['type'].type_obj}' and '{_expr['type']}':{_line}") 
                  expr = {
                        'expr' : '%s[%s] = %s;' % (_name['expr'],_index['expr'],_expr['expr']),
                        'type' : _name['type'].type_obj
                  }
                  return expr
            
            # <name>[<expr>].<name> = <expr>;
            if node[0] == 'assign_var_index_struct':
                  _name = self.walk(node[1])
                  _index = self.walk(node[2])
                  _field = node[3]
                  _expr = self.walk(node[4])
                  _line = node[5]

                  if not isinstance(_name['type'],Array) :
                        HascalError(f"'{_name['type']}' is not subscriptable:{_line}")
                  
                  if not isinstance(_name['type'].type_obj,Struct) :
                        HascalError(f"'{_name['type']}' is not a struct:{_line}")
                  
                  if not _field in _name['type'].type_obj.members :
                        HascalError(f"'{_name['type']}' has no field '{_field}':{_line}")

                  if is_compatible_type(_name['type'].type_obj.members[_field],_expr['type']) == False:
                        HascalError(f"Mismatched type '{_name['type'].type_obj.members[_field]}' and '{_expr['type']}':{_line}")

                  expr = {
                        'expr' : '%s[%s].%s = %s;' % (_name['expr'],_index['expr'],_field,_expr['expr']),
                        'type' : _name['type'].type_obj.members[_field]
                  }
                  return expr
            
            # *<name> = <expr>
            if node[0] == 'assign_ptr' :
                  _name = self.walk(node[1])
                  _type = _name['type']
                  _expr = self.walk(node[2])
                  _line = node[3]

                  if not _type.is_ptr :
                        HascalError(f"Invalid type argument of unary '*' (have '{_type['type']}'):{_line}")
                  _type.is_ptr = False
                  _type.ptr_str = ''
                  if is_compatible_type(_type,_expr['type']) == False :
                        HascalError(f"Mismatched type '{_type}' and '{_expr['type']}':{_line}")
                  expr = {
                        'expr' : "*%s = %s;\n" % (_name['expr'],self.walk(node[2])['expr']),
                        'type' : _type,
                  }
                  return expr
            #-----------------------------------------
            # return <expr>
            if node[0] == 'return':
                  _expr = self.walk(node[1])
                  _line = node[2]

                  if _expr['expr'] in self.types :
                        HascalError(f"Cannot return a type '{_expr['expr']}':{_line}")
                  
                  expr = {
                        'expr' : "return %s;\n" %  _expr['expr'],
                        'type' : _expr['type'],
                        'return' : True
                  }
                  return expr 
            #-----------------------------------------
            # break
            if node[0] == 'break':
                  expr = {
                        'expr' : 'break;\n',
                        'type' : '',
                  }
                  return expr
            
            # continue
            if node[0] == 'continue':
                  expr = {
                        'expr' : 'continue;\n',
                        'type' : '',
                  }
                  return expr
            #-----------------------------------------
            # use <lib_name>
            if node[0] == 'use':
                  if node[1] in self.imported :
                        ...
                  if sys.platform.startswith('win'):
                        name = '.'.join(name for name in node[1])
                        if name.startswith("libcpp.") :
                              path = node[1]
                              final_path = str(self.BASE_DIR+"\\hlib\\")

                              ends_of_path = path[-1]
                              for x in path[:-1]:
                                    final_path += x + "\\"
                              final_path_ld = final_path + ends_of_path + ".ld"
                              # final_path_wld = final_path + ends_of_path + ".wld"
                              final_path_h = final_path + ends_of_path + ".hpp"
                              final_path += ends_of_path + ".cc"
                              try:
                                    with open(final_path, 'r') as fd:
                                          cpp_code = fd.read()
                                          with open(final_path_h,'r') as fh :
                                                hpp_code = fh.read()
                                                self.imported.append(name)
                                                self.add_to_output(cpp_code,hpp_code)
                              except FileNotFoundError:
                                    HascalError(f"cannot found '{name}' library. Are you missing a library ?")
                              # if isfile(final_path_wld):
                              #       with open(final_path_ld) as f:
                              #             ld = f.read().split(',')
                              #             self.LDFLAGS += ld  
                              if isfile(final_path_ld):
                                    with open(final_path_ld) as f:
                                          ld = list(f.read().split(','))
                                          for i in ld :
                                                self.LDFLAGS.append(i)                                   
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
                                          
                                          generator = Generator(self.BASE_DIR)
                                          output_cpp = generator.generate(tree,True)

                                          self.imported.append(name)
                                          self.imported += generator.imported
                                          self.add_to_output(output_cpp,generator.src_includes)
                                          self.funcs.update(generator.funcs)
                                          self.types.update(generator.types)
                                          self.vars.update(generator.vars)
                              except FileNotFoundError:
                                    HascalError(f"cannot found '{name}' library. Are you missing a library ?")            
                  else :
                        name = '.'.join(name for name in node[1])
                        if name.startswith("libcpp.") :
                              path = node[1]
                              final_path = str(self.BASE_DIR+"/hlib/")

                              ends_of_path = path[-1]
                              for x in path[:-1]:
                                    final_path += x + "/"
                              final_path_ld = final_path + ends_of_path + ".ld"
                              final_path_h = final_path + ends_of_path + ".hpp"
                              final_path += ends_of_path + ".cc"
                              try:
                                    with open(final_path, 'r') as fd:
                                          cpp_code = fd.read()
                                          with open(final_path_h,'r') as fh :
                                                hpp_code = fh.read()
                                                self.imported.append(name)
                                                self.add_to_output(cpp_code,hpp_code)
                              except FileNotFoundError:
                                    HascalError(f"cannot found '{name}' library. Are you missing a library ?")
                              if isfile(final_path_ld):
                                    with open(final_path_ld) as f:
                                          ld = list(f.read().split(','))
                                          for i in ld :
                                                self.LDFLAGS.append(i)    
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
                                          generator = Generator(self.BASE_DIR)
                                          output_cpp = generator.generate(tree,True)

                                          self.imported.append(name)
                                          self.imported += generator.imported
                                          self.add_to_output(output_cpp,generator.src_includes)
                                          self.funcs.update(generator.funcs)
                                          self.types.update(generator.types)
                                          self.vars.update(generator.vars)
                              except FileNotFoundError:
                                    HascalError(f"cannot found '{name}' library. Are you missing a library ?")
                  return {'expr':'','type':''}
            
            # local use <lib_name>
            if node[0] == 'use_local':
                  if sys.platform.startswith('win32'):
                        name = '.'.join(name for name in node[1])
                        if name.startswith("cpp."):
                              path = name.split('.')
                              final_path = ""

                              ends_of_path = path[-1]
                              for x in path[:-1]:
                                    final_path += x + "\\"
                              final_path_ld = final_path + ends_of_path + ".ld"
                              final_path_h = final_path + ends_of_path + ".hpp"
                              final_path += ends_of_path + ".cc"

                              try:
                                    with open(final_path, 'r') as fd:
                                          cpp_code = fd.read()
                                          with open(final_path_h,'r') as fh :
                                                hpp_code = fh.read()
                                                self.imported.append(name)
                                                self.add_to_output(cpp_code,hpp_code)
                              except FileNotFoundError:
                                    HascalError(f"cannot found '{name}' library. Are you missing a library ?")
                              if isfile(final_path_ld):
                                    with open(final_path_ld) as f:
                                          ld = f.read().split(',')
                                          self.LDFLAGS += ld  

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
                                          generator = Generator(HLIB_BASE_DIR)
                                          output_cpp = generator.generate(tree,True)

                                          self.imported.append(name)
                                          self.imported += generator.imported
                                          self.add_to_output(output_cpp, generator.src_includes)
                                          self.funcs.update(generator.funcs)
                                          self.types.update(generator.types)
                                          self.vars.update(generator.vars)
                              except FileNotFoundError:
                                    HascalError(f"cannot found '{name}' library. Are you missing a library ?")
                              
                  elif sys.platform.startswith('linux'):
                        name = '.'.join(name for name in node[1])
                        if name.startswith("cpp."):
                              path = name.split('.')
                              final_path = ""

                              ends_of_path = path[-1]
                              for x in path[:-1]:
                                    final_path += x + "/"
                              final_path_h = final_path + ends_of_path + ".hpp"
                              final_path += ends_of_path + ".cc"

                              try:
                                    with open(final_path, 'r') as fd:
                                          cpp_code = fd.read()
                                          with open(final_path_h,'r') as fh :
                                                hpp_code = fh.read()
                                                self.imported.append(name)
                                                self.add_to_output(cpp_code,hpp_code)
                              except FileNotFoundError:
                                    HascalError(f"cannot found '{name}' library. Are you missing a library ?")

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
                                          generator = Generator(HLIB_BASE_DIR)
                                          output_cpp = generator.generate(tree,True)

                                          self.imported.append(name)
                                          self.imported += generator.imported
                                          self.add_to_output(output_cpp, generator.src_includes)
                                          self.funcs.update(generator.funcs)
                                          self.types.update(generator.types)
                                          self.vars.update(generator.vars)
                              except FileNotFoundError:
                                    HascalError(f"cannot found '{name}' library. Are you missing a library ?")
                  return {'expr':'','type':''}
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
                  current_vars = self.vars.copy()
                  current_types = self.types.copy()
                  _gtypes = self.walk(node[5])

                  _name = node[2]
                  _type = self.walk(node[1])
                  _return_type = _type['expr']
                  _params = { }

                  params = self.walk(node[3])
                  params_type = params['type']
                  params_name = params['name']

                  if len(params) != 1:
                        for i in range(len(params_name)):
                              _params[params_name[i]] = params_type[i]
                              self.vars[params_name[i]] = Var(params_name[i],params_type[i])

                  if params['expr'].endswith(','):
                        params['expr'] = params['expr'][:-1]


                  if self.funcs.get(_name) != None:
                        if type(self.funcs[_name]) == Function:
                              self.funcs[_name] = [self.funcs[_name],Function(_name,_params,_type['type'])]
                        else:
                              self.funcs[_name].append(Function(_name,_params,_type['type']))
                  else :
                        self.funcs[_name] = Function(_name,_params,_type['type'])

                  _name = node[2]
                  _expr = self.walk(node[4])
                  _res = ""

                  if _return_type != 'void' and len(_expr) < 1 :
                        HascalError(f"Function '{_name}' must return a value at end of function block")
                  if _return_type != 'void' and len(_expr) != 0 and _expr[-1].get('return') != True :
                        HascalError(f"Function '{_name}' should return a value at end of function block")
                  if _return_type != 'int' and _name == 'main':
                        HascalError(f"Function 'main' must return 'int'")
                  
                  for e in _expr :
                        _res += e['expr']
                  res = "%s %s %s(%s) {\n%s\n}\n" % (_gtypes['expr'],_return_type,_name,params['expr'],_res) 

                  self.vars = current_vars
                  self.types = current_types

                  # program arguments 
                  _params_keys = list(_params.keys())
                  if len(params['name']) == 1 and (_name == "main" and isinstance(_params[_params_keys[0]],Array) and isinstance(_params[_params_keys[0]],Type) and _params[_params_keys[0]].type_obj.type_name == 'string'):
                        res = "%s %s %s(int argc,char** args) {\nstd::vector<std::string> %s;for(int i=0;i<argc;i++){%s.push_back(args[i]);}\n%s\n}\n" % (_gtypes['expr'],_return_type,_name,_params_keys[0],_params_keys[0],_res) 
                        expr = {
                              'expr' : res,
                              'type' : _type['type'],
                        }
                        return expr
                  
                  if len(params['name']) > 1 and _name == "main" :
                        HascalError(f"Function 'main' takes only zero or one arguments(with string array type)")
                  if len(params['name']) == 1 and ((isinstance(_params[_params_keys[0]],Array) and isinstance(_params[_params_keys[0]].type_obj,Struct)) or isinstance(_params[_params_keys[0]],Struct)) and _name == "main" :
                        HascalError(f"Function 'main' takes only zero or one arguments(with struct type)")
                  if len(params['name']) == 1 and _name == "main" and isinstance(_params[_params_keys[0]],Array) and _params[_params_keys[0]].type_obj.type_name != 'string' :
                        HascalError(f"Function 'main' takes only zero or one arguments(with string array type)")
                  
                  expr = {
                        'expr' : res,
                        'type' : _type['type'],
                  }
                  return expr
            #-------------------------------------
            if node[0] == "inline_function" :
                  _name = node[2]
                  _type = self.walk(node[1])
                  _params = { }

                  params = self.walk(node[3])
                  params_type = params['type']
                  params_expr = params['expr']
                  params_name = params['name']
                        
                  if len(params) != 1:
                        for i in params_name :
                              for j in params_type :
                                    _params[i] = j   
                  
                  if self.funcs.get(_name) != None:
                        if type(self.funcs[_name]) == Function:
                              self.funcs[_name] = [self.funcs[_name],Function(_name,_params,_type['type'])]
                        else:
                              self.funcs[_name].append(Function(_name,_params,_type['type']))
                  else :
                        self.funcs[_name] = Function(_name,_params,_type['type'])

                  return {'expr':'','type':'type'}
            #-------------------------------------
            # struct <name> {
            #     <block_struct>
            # }
            if node[0] == 'struct':
                  _name = node[1]
                  _members = { }
                  self.types[_name] = Struct(_name,_members)
                  _body = self.walk(node[2])
                  _line = node[3]
                  # generate output code and members
                  res = ""
                  for e in _body :
                        if str(e['type']) == _name :
                              HascalError(f"Incomplete type definition '{_name}':{_line}")
                        
                        if e.get('cuse') == None :
                              _members[e['name']] = e['type']

                        res += e['expr']
                  self.types[_name] = Struct(_name,_members)
                  expr = {
                        'expr' : 'struct %s{\n%s\n};\n' % (_name,res),
                        'type' : _name,
                  } 
                  return expr
            
            # struct <name> : <name> {
            #     <block_struct>
            # }
            if node[0] == 'struct_inheritance':
                  _name = node[1]
                  _i_name = node[2]
                  _line = node[4]
                  _members = { }
                  self.types[_name] = Struct(_name,_members)
                  _body = self.walk(node[3])

                  # get members from parent struct
                  if self.types.get(_i_name) != None:
                        _members = self.types[_i_name].members
                  else :
                        HascalError(f"Cannot found struct '{_i_name}'")

                  # generate output code and member
                  res = ""
                  for e in _body :
                        if str(e['type']) == _name :
                              HascalError(f"Incomplete type definition '{_name}':{_line}")
                        
                        if e.get('cuse') == None :
                              _members[e['name']] = e['type']

                        res += e['expr']
                        
                  self.types[_name] = Struct(_name,_members)
                  expr = {
                        'expr' : 'struct %s : %s{\n%s\n};\n' % (_name,_i_name,res),
                        'type' : _name,
                  } 
                  return expr
            #-------------------------------------
            # enum <name> {
            #     <enum_names>
            # }
            if node[0] == 'enum':
                  _name = node[1]
                  _members = node[2]
                  self.types[_name] = Enum(_name,_members)
                  expr = {
                        'expr' : 'enum %s{\n%s\n}\n' % (_name,_members),
                        'type' : _name,
                  } 
                  return expr
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
                  cuurent_vars = self.vars.copy()
                  cond = self.walk(node[1])
                  body = self.walk(node[2])

                  res = ""
                  for e in body :
                        res += e['expr']

                  self.vars = cuurent_vars
                  expr = {
                        'expr' : 'if(%s){\n%s\n}\n' % (cond['expr'],res),
                        'type' : '',
                  }
                  return expr
            if node[0] == 'if_else':
                  cuurent_vars = self.vars.copy()
                  cond = self.walk(node[1])
                  body = self.walk(node[2])
                  body2 = self.walk(node[3])

                  res = ""
                  for e in body :
                        res += e['expr']
                  res2 = ""
                  for e in body2 :
                        res2 += e['expr']

                  self.vars = cuurent_vars
                  expr = {
                        'expr' : 'if(%s){\n%s\n}else {\n%s\n}\n' % (cond['expr'],res,res2),
                        'type' : '',
                  }
                  return expr
            if node[0] == 'if_else2':
                  cuurent_vars = self.vars.copy()
                  cond = self.walk(node[1])
                  body = self.walk(node[2])
                  body2 = self.walk(node[3])
                  res = ""
                  for e in body :
                        res += e['expr']

                  self.vars = cuurent_vars
                  expr = {
                        'expr' : 'if(%s){\n%s\n}else %s\n' % (cond['expr'],res,body2['expr']),
                        'type' : '',
                  }
                  return expr
            #------------------------------------
            # for <name> in <name> {
            #     <block>
            # }
            if node[0] == 'for':      
                  _name = node[1]
                  # todo
                  _name2 = node[2][0]
                  _line = node[4]
                  res = ""
                  current_vars = self.vars.copy()

                  if not (_name2 in self.vars or _name2 in self.consts) :
                        HascalError(f"'{_name2}' not defined:{_line}") #todo

                  if not isinstance(self.vars[_name2].type,Array) :
                        HascalError(f"'{_name2}' is not iterable:{_line}") 

                  self.vars[_name] = Var(_name,self.vars[_name2].type.type_obj)
                  body = self.walk(node[3])
                  for e in body :
                        res += e['expr']
                  self.vars = current_vars
                  expr = {
                        'expr' : 'for(auto %s : %s){\n%s\n}\n' % (_name,_name2,res),
                        'type' : '',
                  }
                  return expr
            #--------------------------------------
            # while <condition> {
            #     <block>
            # }
            if node[0] == 'while':      
                  cond = self.walk(node[1])
                  body = self.walk(node[2])
                  res = ""
                  for e in body :
                        res += e['expr']
                  expr = {
                        'expr' : 'while(%s){\n%s\n}\n' % (cond['expr'],res),
                        'type' : '',
                  }
                  return expr
            #---------------------------------------
            if node[0] == 'cast' :
                  _return_type = self.walk(node[1])
                  _expr = self.walk(node[2])
                  _line = node[3]

                  expr = {
                        'expr' : 'static_cast<%s>(%s)' % (_return_type['type'],_expr['expr']),
                        'type' : _return_type['type'],
                  }
                  return expr
            #---------------------------------------
            if node[0] == 'pass_by_ptr' :
                  _name = self.walk(node[1])
                  _type = _name['type']
                  _line = node[2]
                  
                  if not _type.is_ptr :
                        HascalError(f"Invalid type argument of unary '*' (have '{_type}'):{_line}")
                  
                  type_ = Type(_type.type_name,_type.stdtype,is_ptr=False,ptr_str='',category=_type.category)

                  expr = {
                        'expr' : '*%s' % (_name['expr']),
                        'type' : type_,
                  }
                  return expr
            
            if node[0] == 'pass_by_ref' :
                  _name = self.walk(node[1])
                  _type = _name['type']
                  _line = node[2]

                  type_ = Type(_type.type_name,_type.stdtype,is_ptr=True,ptr_str='*',category=_type.category)

                  expr = {
                        'expr' : '&%s' % (_name['expr']),
                        'type' : type_,
                  }
                  return expr
            #---------------------------------------
            # <expr>                   
            if node[0] == 'expr':
                  _expr = self.walk(node[1])
                  expr = {
                        'expr' : "%s;\n" % (_expr['expr']),
                        'type' : _expr['type'],
                  }
                  return expr
            #---------------------------------------
            # <expr>(<params>)
            if node[0] == 'call':
                  _name = node[1]
                  _line = node[3]
                  _args = [self.walk(_arg) for _arg in node[2]]
                  if self.exists(_name):
                        if _name == "print":
                              expr = {
                                    'expr' : 'std::cout << %s << std::endl' % ('<< '.join(self.walk(arg)['expr'] for arg in node[2])),
                                    'type' : self.funcs['print'].return_type,
                              }
                              return expr
                        else :
                              if isinstance(self.funcs.get(_name),list):
                                    _f_params = {}
                                    for f in self.funcs[_name]:
                                          _f_params[f.name] = f.params
                                    
                                    counter = 0
                                    while counter < len(self.funcs[_name]):
                                          f = self.funcs[_name][counter]

                                          if len(f.params) != len(node[2]):
                                                # check if there is at end of list
                                                if counter == len(self.funcs[_name]) - 1:
                                                      if len(f.params) > len(node[2]):
                                                            HascalError(f"{_name} has more parameters than given:{_line}")
                                                      else :
                                                            HascalError(f"{_name} has less parameters than given:{_line}")
                                                else :
                                                      counter += 1
                                                      continue
                                          else :
                                                _return_type = f.return_type
                                                if isinstance(f.return_type,Generic):
                                                      keys = list(f.params.keys())
                                                      for i in range(len(f.params)):
                                                            if isinstance(f.params[keys[i]],Generic):
                                                                  if f.params[keys[i]].type_name == f.return_type.type_name:
                                                                        _return_type = _args[i]['type']
                                                                        break
                                                # check if return type is pointer
                                                if isinstance(_return_type,Type) and _return_type.is_ptr:
                                                      _return_type = Type(_return_type.type_name,_return_type.stdtype,is_ptr=True,ptr_str=_return_type.ptr_str,category=_return_type.category)
                                                
                                                expr = {
                                                      'expr' : '%s(%s)' % (f.name,','.join(self.walk(arg)['expr'] for arg in node[2])),
                                                      'type' : _return_type,
                                                }
                                                return expr
                                          counter += 1
                              if _name in self.types:
                                    if not isinstance(self.types[_name],Struct):
                                          HascalError(f"Cannot call type {_name}:{_line}")
                                    
                                    expr = {
                                          'expr' : "%s{%s}" % (_name, ', '.join(self.walk(arg)['expr'] for arg in node[2])),
                                          'type' : self.types[_name],
                                    }
                                    return expr
                              else :
                                    _return_type = self.funcs[_name].return_type
                                    if isinstance(self.funcs[_name].return_type,Generic):
                                          keys = list(self.funcs[_name].params.keys())
                                          for i in range(len(self.funcs[_name].params)):
                                                if isinstance(self.funcs[_name].params[keys[i]],Generic):
                                                      if self.funcs[_name].params[keys[i]].type_name == self.funcs[_name].return_type.type_name:
                                                            _return_type = _args[i]['type']
                                                            break
                                    # check if return type is pointer
                                    if isinstance(_return_type,Type) and _return_type.is_ptr:
                                          _return_type = Type(_return_type.type_name,_return_type.stdtype,is_ptr=True,ptr_str=_return_type.ptr_str,category=_return_type.category)
                                                
                                    expr = {
                                          'expr' : "%s(%s)" % (_name, ', '.join(self.walk(arg)['expr'] for arg in node[2])),
                                          'type' : _return_type,
                                    }
                                    return expr
                  else :
                        HascalError(f"Function '{_name}' not defined:{_line}")
            # --------------operators-----------------
            # todo : error if string *-/ string
            # <expr> + <expr>
            if node[0] == 'add':
                  _expr0 = self.walk(node[1])
                  _expr1 = self.walk(node[2])
                  _line = node[3]
                  if str(_expr0['type']) != str(_expr1['type']) :
                        HascalError(f"Mismatched type {_expr0['type']} and {_expr1['type']}:{_line}")
                        
                  else :
                        expr = {
                              'expr' : '%s + %s' % (_expr0['expr'],_expr1['expr']),
                              'type' : _expr0['type'] # or : _expr1['type']
                        }
                        return expr

            # <expr> - <expr>
            if node[0] == 'sub':
                  _expr0 = self.walk(node[1])
                  _expr1 = self.walk(node[2])
                  _line = node[3]

                  if str(_expr0['type']) != str(_expr1['type']) :
                        HascalError(f"Mismatched type {_expr0['type']} and {_expr1['type']}:{_line}.")  
                  else :
                        expr = {
                              'expr' : '%s - %s' % (_expr0['expr'],_expr1['expr']),
                              'type' : _expr0['type'] # or : _expr1['type']
                        }
                        return expr

            # <expr> * <expr>
            if node[0] == 'mul':
                  _expr0 = self.walk(node[1])
                  _expr1 = self.walk(node[2])
                  _line = node[3]

                  if str(_expr0['type']) != str(_expr1['type']) :
                        HascalError(f"Mismatched type {_expr0['type']} and {_expr1['type']}:{_line}") 
                  else :
                        expr = {
                              'expr' : '%s * %s' % (_expr0['expr'],_expr1['expr']),
                              'type' : _expr0['type'] # or : _expr1['type']
                        }
                        return expr

            # <expr> / <expr>
            if node[0] == 'div':
                  _expr0 = self.walk(node[1])
                  _expr1 = self.walk(node[2])
                  _line = node[3]

                  if str(_expr0['type']) != str(_expr1['type']) :
                        HascalError(f"Mismatched type {_expr0['type']} and {_expr1['type']}:{_line}") 
                  else :
                        expr = {
                              'expr' : '%s / %s' % (_expr0['expr'],_expr1['expr']),
                              'type' : _expr0['type'] # or : _expr1['type']
                        }
                        return expr

            # (<expr>)
            if node[0] == 'paren_expr':
                  _expr = self.walk(node[1])
                  expr = {
                        'expr' : '(%s)' % (_expr['expr']),
                        'type' : _expr['type'] 
                  }
                  return expr
            
            # --------------end of operators-----------------  

            # ---------------conditions---------------------
            # <condition>
            if node[0] == 'cond':
                  _expr0 = self.walk(node[1])

                  expr = {
                        'expr' : '%s' % (_expr0['expr']),
                        'type' : _expr0['type'] 
                  }
                  return expr

            # not <condition>
            if node[0] == 'not':
                  _expr0 = self.walk(node[1])

                  expr = {
                        'expr' : '!%s' % (_expr0['expr']), # may have bug
                        'type' : _expr0['type'] 
                  }
                  return expr

            # <condition> and <condition>
            if node[0] == 'and':
                  _expr0 = self.walk(node[1])
                  _expr1 = self.walk(node[2])
                  _line = node[3]

                  expr = {
                        'expr' : '%s && %s' % (_expr0['expr'],_expr1['expr']),
                        'type' : _expr0['type'] # or : _expr1['type']
                  }
                  return expr

            # <condition> or <condition>
            if node[0] == 'or':
                  _expr0 = self.walk(node[1])
                  _expr1 = self.walk(node[2])
                  _line = node[3]
                  expr = {
                        'expr' : '%s || %s' % (_expr0['expr'],_expr1['expr']),
                        'type' : _expr0['type'] # or : _expr1['type']
                  }
                  return expr

            # <expr> == <expr>
            if node[0] == 'equals':
                  _expr0 = self.walk(node[1])
                  _expr1 = self.walk(node[2])
                  _line = node[3]
                  if str(_expr0['type']) != str(_expr1['type']) :
                        HascalError(f"Mismatched type {_expr0['type']} and {_expr1['type']}:{_line}")
                  # todo : check if type is int or bool else error  
                  else :
                        expr = {
                              'expr' : '%s == %s' % (_expr0['expr'],_expr1['expr']),
                              'type' : _expr0['type'] # or : _expr1['type']
                        }
                        return expr

            # <expr> != <expr>
            if node[0] == 'not_equals':
                  _expr0 = self.walk(node[1])
                  _expr1 = self.walk(node[2])
                  _line = node[3]

                  if str(_expr0['type']) != str(_expr1['type']) :
                        HascalError(f"Mismatched type {_expr0['type']} and {_expr1['type']}:{_line}")
                  # todo : check if type is int or bool else error  
                  else :
                        expr = {
                              'expr' : '%s != %s' % (_expr0['expr'],_expr1['expr']),
                              'type' : _expr0['type'] # or : _expr1['type']
                        }
                        return expr

            # <expr> >= <expr>
            if node[0] == 'greater_equals':
                  _expr0 = self.walk(node[1])
                  _expr1 = self.walk(node[2])
                  _line = node[3]

                  if str(_expr0['type']) != str(_expr1['type']) :
                        HascalError(f"Mismatched type {_expr0['type']} and {_expr1['type']}:{_line}")
                  # todo : check if type is int or bool else error  
                  else :
                        expr = {
                              'expr' : '%s >= %s' % (_expr0['expr'],_expr1['expr']),
                              'type' : _expr0['type'] # or : _expr1['type']
                        }
                        return expr

            # <expr> <= <expr>
            if node[0] == 'less_equals':
                  _expr0 = self.walk(node[1])
                  _expr1 = self.walk(node[2])
                  _line = node[3]

                  if str(_expr0['type']) != str(_expr1['type']) :
                        HascalError(f"Mismatched type {_expr0['type']} and {_expr1['type']}:{_line}")
                  # todo : check if type is int or bool else error  
                  else :
                        expr = {
                              'expr' : '%s <= %s' % (_expr0['expr'],_expr1['expr']),
                              'type' : _expr0['type'] # or : _expr1['type']
                        }
                        return expr
            
            # <expr> > <expr>
            if node[0] == 'greater':
                  _expr0 = self.walk(node[1])
                  _expr1 = self.walk(node[2])
                  _line = node[3]

                  if str(_expr0['type']) != str(_expr1['type']) :
                        HascalError(f"Mismatched type {_expr0['type']} and {_expr1['type']}:{_line}")
                  # todo : check if type is int or bool else error  
                  else :
                        expr = {
                              'expr' : '%s > %s' % (_expr0['expr'],_expr1['expr']),
                              'type' : _expr0['type'] # or : _expr1['type']
                        }
                        return expr

            # <expr> < <expr>
            if node[0] == 'less':
                  _expr0 = self.walk(node[1])
                  _expr1 = self.walk(node[2])
                  _line = node[3]
                  
                  if str(_expr0['type']) != str(_expr1['type']) :
                        HascalError(f"Mismatched type {_expr0['type']} and {_expr1['type']}:{_line}")
                  # todo : check if type is int or bool else error    
                  else :
                        expr = {
                              'expr' : '%s < %s' % (_expr0['expr'],_expr1['expr']),
                              'type' : _expr0['type'] # or : _expr1['type']
                        }
                        return expr

            # not <expr>
            if node[0] == 'not_cond':
                  _expr0 = self.walk(node[1])
                  expr = {
                        'expr' : '!%s' % (_expr0['expr']), # may have bug
                        'type' : _expr0['type'] 
                  }
                  return expr

            # true / false
            if node[0] == 'bool_cond':
                  expr = {
                        'expr' : '%s' % (node[1]),
                        'type' : 'bool',
                  }
                  return expr
            
            # <expr>
            if node[0] == 'expr_cond':
                  _expr = self.walk(node[1])
                  expr = {
                        'expr' : '%s' % (_expr['expr']), # may have bug
                        'type' : _expr['type'] 
                  }
                  return expr
            
            # <expr>
            if node[0] == 'paren_cond':
                  _expr = self.walk(node[1])
                  expr = {
                        'expr' : '(%s)' % (_expr['expr']), # may have bug
                        'type' : _expr['type'] 
                  }
                  return expr
            # ---------------end of conditions---------------------     
            # <name>
            if node[0] == 'var':
                  _name = node[1][0]
                  _line = node[2]
                  if len(node[1]) == 1:
                        if _name in self.vars:
                              expr = {
                                    'expr' : "%s" % (_name),
                                    'type' : self.vars[_name].type,
                                    'obj' : self.vars[_name]
                              }
                              return expr
                        elif _name in self.consts :
                              expr = {
                                    'expr' : "%s" % (_name),
                                    'type' : self.consts[_name].type,
                                    'obj' : self.consts[_name]
                              }
                              return expr
                        elif _name in self.types :
                              expr = {
                                    'expr' : "%s" % (_name),
                                    'type' : self.types[_name],
                                    'obj' : self.types[_name]
                              }
                              return expr
                        elif _name in self.funcs :
                              expr = {
                                    'expr' : "%s" % (_name),
                                    'type' : '', # todo : return function
                                    'obj' : self.funcs[_name]
                              }
                              return expr
                        else :
                              HascalError(f"'{_name}' is not reachable or not defined:{_line}")
                  else :
                        _full_name = ''

                        if _name in self.vars:
                              if self.vars[_name].type.is_ptr :
                                    _full_name += _name + '->'
                              else :
                                    _full_name += _name + '.'
                              
                              if isinstance(self.vars[_name].type,Struct) :
                                    # if struct has no member show error else set current member to _current_member
                                    if self.vars[_name].type.members == {} :
                                          HascalError(f"Struct '{_name}' have not any members:{_line}")
                                    _members = self.vars[_name].type.members

                                    _back_member_name = _name
                                    _back_member_type = self.vars[_name].type

                                    for i in range(len(node[1])):
                                          # check if node[1][i] is a member of struct and check it is not first member
                                          if node[1][i] in _members and i != 0 :
                                                _current_member = node[1][i]

                                                # check if current member is a struct
                                                if isinstance(_members[_current_member],Struct) :
                                                      # if struct has no member show error else set _members to _members[_current_member]
                                                      if _members[_current_member].members == {} :
                                                            HascalError(f"Struct '{_name}' have not any members:{_line}")

                                                      # check if current member is the last member of node[1]
                                                      if i == len(node[1])-1 :
                                                            _full_name += _current_member
                                                            expr = {
                                                                  'expr' :  "%s" % (_full_name),
                                                                  'type' : _members[_current_member],
                                                            }
                                                            return expr
                                                      if _members[_current_member].is_ptr :
                                                            _full_name += _current_member + '->'
                                                      else :
                                                            _full_name += _current_member + '.'
                                                      
                                                      _members = _members[_current_member].members
                                                      continue
                                                      
                                                else :
                                                      if not _current_member in _members :
                                                            HascalError(f"Struct '{node[1][i-1]}' has no member named '{_current_member}':{_line}")

                                                      _full_name += _current_member
                                                      expr = {
                                                            'expr' : "%s" % (_full_name),
                                                            'type' : _members[_current_member],
                                                      }
                                                      return expr
                                          elif i == 0 :    
                                                continue
                                          else :
                                                HascalError(f"Struct '{node[1][i-1]}' has no member named '{_current_member}':{_line}")  

                              elif str(self.vars[_name].type).startswith('std::vector'):
                                    expr = {
                                          'expr' : "%s" % (_full_name),
                                          'type' : self.types[str(self.vars[_name].type).split('<')[1].split('>')[0]],
                                    }
                                    return expr  
                              expr = {
                                    'expr' : "%s" % (_full_name),
                                    'type' : self.vars[_name].type,
                              }
                              return expr
                        elif _name in self.consts :
                              if isinstance(self.types[str(self.vars[_name].type)],Struct) :
                                    # if struct has no member show error else set current member to _current_member
                                    if self.types[self.consts[_name].type].members == {} :
                                          HascalError(f"Struct '{_name}' has no member:{_line}")
                                    _members = self.types[self.consts[_name].type].members

                                    for i in range(len(node[1])-1):
                                          # check if node[1][i] is a member of struct and check it is not first member
                                          if node[1][i] in _members and i != 0 :
                                                _current_member = node[1][i]
                                          
                                                # check if current member is a struct
                                                if isinstance(_members[_current_member],Struct) :
                                                      # if struct has no member show error else set _members to _members[_current_member]
                                                      if _members[_current_member].members == {} :
                                                            HascalError(f"Struct '{_name}' has no member:{_line}")
                                                
                                                      # check if current member is the last member of node[1]
                                                      if i == len(node[1])-1 :
                                                            # check if current member is an vector
                                                            if not _members[_current_member].type.startswith('std::vector') :
                                                                  HascalError(f"Struct '{_name}' has no member:{_line}")

                                                            expr = {
                                                                  'expr' :  "%s" % (_full_name),
                                                                  'type' : _members[_current_member],
                                                            }
                                                            return expr
                                                      _members = _members[_current_member].members
                                                      continue
                                                else :
                                                      if not _current_member in _members :
                                                            HascalError(f"Struct '{_name}' has no member:{_line}")
                                                      if not _members[_current_member].type.startswith('std::vector') :
                                                                  HascalError(f"Struct '{_name}' has no member:{_line}")

                                                      expr = {
                                                            'expr' : "%s" % (_full_name),
                                                            'type' : _members[_current_member],
                                                      }
                                                      return expr
                                          elif i == 0 : ...
                                          else :
                                                HascalError(f"'{node[1][i]}' is not a member of '{_name}':{_line}")  

                              if str(self.consts[_name].type).startswith('std::vector'):
                                    expr = {
                                          'expr' : "%s" % (_name),
                                          'type' : self.types[str(self.consts[_name].type).split('<')[1].split('>')[0]],
                                    }
                                    return expr  

                              expr = {
                                    'expr' : "%s" % (_full_name),
                                    'type' : self.consts[_name].type,
                              }
                              return expr
                        else :
                              HascalError(f"'{_name}' is not reachable or not defined:{_line}")                             
            #---------------------------------------
            # <name>[<expr>]
            if node[0] == 'var_index':
                  _name = self.walk(node[1])
                  _expr = self.walk(node[2])
                  _line = node[3]

                  if isinstance(_name['type'],Array) :
                        expr = {
                              'expr' : "%s[%s]" % (_name['expr'],_expr['expr']),
                              'type' : _name['type'].type_obj,
                        }
                        return expr
                  elif str(_name['type']) == 'string' :
                        expr = {
                              'expr' : "%s[%s]" % (_name['expr'],_expr['expr']),
                              'type' : self.types['char'],
                        }
                        return expr
                  else :
                        HascalError(f"'{_name['expr']}' is not subscriptable:{_line}")
            #-------------------------------------------
            # <expr>, <expr>
            if node[0] == 'exprs':
                  _expr0 = self.walk(node[1])
                  _expr1 = self.walk(node[2])
                        
                  expr = {
                        'expr' : '%s,%s' % (_expr0['expr'],_expr1['expr']),
                        'type' : _expr0['type'] # or : _expr1['type']
                  }
                  return expr
            # [<expr>]
            if node[0] == 'list':
                  _expr = self.walk(node[1])
                  expr = {
                        'expr' : '{%s}' % (_expr['expr']),
                        'type' : Array(_expr['type']),
                  }
                  return expr
            #-------------------------------------------
            # <expr>.<name>
            if node[0] == '.':
                  _expr = self.walk(node[1])
                  _name = node[2]

                  expr = {
                        'expr' : '%s.%s' % (_expr['expr'],_name),
                        'type' : _expr['type'], # todo : return _name type
                  }
                  return expr
            # <expr>.<name>
            if node[0] == '.2':
                  # todo : name type and index type check
                  _expr0 = self.walk(node[1])
                  _expr1 = self.walk(node[3])
                  _name = node[2]

                  expr = {
                        'expr' : '%s.%s[%s]' % (_expr0['expr'],_name,_expr1['expr']),
                        'type' : _expr['type'], # todo : return _name type
                  }
                  return expr
            #--------------------------------------------
            if node[0] == 'generic_params_no' :
                  expr = {
                        'expr' : '',
                        'type' : [],
                        'name' : [],
                  }
                  return expr
            
            if node[0] == 'generic_param' :
                  _name = node[1]
                  _line = node[2]

                  if _name in self.types :
                        HascalError(f"Type '{_name}' is already defined:{_line}")

                  expr = {
                        'expr' : "typename %s," % (_name),
                        'type' : Generic(_name),
                        'name' : _name,
                  }
                  return expr

            if node[0] == 'generic_params' :
                  _params = self.walk(node[1])
                  _param = self.walk(node[2])

                  expr = {
                        'expr' : '%s %s' % (_params['expr'],_param['expr']),
                        'type' : _params['type'] + [_param['type']],
                        'name' : _params['name'] + [_param['name']],
                  }
                  return expr
            
            if node[0] == 'generic_params1' :
                  _param = self.walk(node[1])

                  expr = {
                        'expr' : '%s' % (_param['expr']),
                        'type' : [_param['type']],
                        'name' : [_param['name']],
                  }
                  return expr
            
            if node[0] == 'generic_type' :
                  _params = self.walk(node[1])
                  params_name = _params['name']
                  params_type = _params['type']
                  params_expr = _params['expr']

                  for i in range(len(params_name)):
                        self.types[params_name[i]] = params_type[i]
                  
                  if params_expr.endswith(',') :params_expr = params_expr[:-1]
                  res = 'template<%s>\n' % (params_expr)
                  if params_expr == '' : res = ''
                  expr = {
                        'expr' : res,
                        'type' : params_type,
                        'name' : params_name,
                  }
                  return expr
            #--------------------------------------------
            # <return_type>
            if node[0] == 'return_type':
                  _type_name = node[1]
                  _line = node[2]

                  if not _type_name in self.types:
                        HascalError(f"{_type_name} is not defined:{_line}")
                  
                  expr = {
                        'expr' : _type_name,
                        'type' : self.types[_type_name],
                        'name' : _type_name,
                  }
                  return expr
            
            # [<return_type>]
            if node[0] == 'return_type_array':
                  _type = self.walk(node[1])
                  _line = node[2]
                  
                  expr = {
                        'expr' : 'std::vector<%s>' % (_type['expr']),
                        'type' : Array(_type['type']),
                        'name' : _type['name'],
                  }
                  return expr
            
            # *<return_type>
            if node[0] == 'ptr_type':
                  _type = self.walk(node[1])
                  _line = node[2]

                  if not _type['name'] in self.types:
                        HascalError(f"{_type['name']} is not defined:{_line}")
                  
                  if isinstance(_type['type'],Struct):
                        expr = {
                              'expr' : "%s*" % (_type['expr']),
                              'type' : Struct(_type['type'].name,_type['type'].members,is_ptr=True,ptr_str='*',category=_type['type'].category),
                              'name' : _type['name'],
                        }
                        return expr
                  expr = {
                        'expr' : "%s*" % (_type['expr']),
                        'type' : Type(_type['type'].type_name,_type['type'].stdtype,is_ptr=True,ptr_str='*',category=_type['type'].category),
                        'name' : _type['name'],
                  }
                  return expr
            #--------------------------------------------
            if node[0] == 'param_no' :
                  expr = {
                        'expr' : '',
                        'type' : [],
                        'name' : [],
                  }
                  return expr
            
            if node[0] == 'param' :
                  _name = node[1]
                  _return_type = self.walk(node[2])
                  _type = _return_type['expr']
                  _type_name = _return_type['name']
                  _line = node[3]
                  
                  expr = {
                        'expr' : '%s %s,' % (_type,_name),
                        'type' : _return_type['type'],
                        'name' : _name,
                  }
                  return expr
            
            if node[0] == 'params' :
                  _params = self.walk(node[1])
                  _param = self.walk(node[2])

                  expr = {
                        'expr' : '%s %s' % (_params['expr'],_param['expr']),
                        'type' : _params['type'] + [_param['type']],
                        'name' : _params['name'] + [_param['name']],
                  }
                  return expr
            #--------------------------------------------
            if node[0] == 'string':
                  expr = {
                        'expr' : 'std::string("%s")' % node[1],
                        'type' : self.types[node[0]],
                  }
                  return expr
            if node[0] == "multiline_string" :
                  expr = {
                        'expr' : 'std::string(R"(%s)")' % node[1],
                        'type' : self.types['string'],
                  }
                  return expr
            if node[0] == 'bool' or node[0] == 'float' or node[0] == 'int':
                  expr = {
                        'expr' : '%s' % node[1],
                        'type' : self.types[node[0]],
                  }
                  return expr

            if node[0] == 'char':
                  expr = {
                        'expr' : '\'%s\'' % node[1],
                        'type' : self.types[node[0]],
                  }
                  return expr         

class Var(object):
      def __init__(self,name,type,is_array=False,members={}):
            self.name = name
            self.type = type
            self.is_array = is_array
            self.members = members

class Const(Var):
      ...

class Function(object):
      def __init__(self,name,params,return_type):
            self.name = name
            self.params = params # type : dict
            self.return_type = return_type

class Struct(object):
      def __init__(self,name,members,category='',is_ptr=False,ptr_str=''):
            self.name = name
            self.members = members
            self.stdtype = False
            self.is_ptr = is_ptr
            self.ptr_str = ptr_str
            self.category = name
      
      def __str__(self):
            return self.get_type_name()

      def get_type_name(self):
            return self.name + self.ptr_str
class Enum(Struct):
      ...

class Type(object):
      def __init__(self,type_name,stdtype,category='',is_ptr=False,ptr_str=''):
            self.type_name = type_name
            self.stdtype = stdtype
            self.is_ptr = is_ptr
            self.ptr_str = ptr_str
            self.category = category
      
      def __str__(self):
            return self.get_type_name()

      def get_type_name(self):
            if self.is_ptr:
                  return '%s%s' % (self.type_name,self.ptr_str)
            else :
                  return self.type_name + self.ptr_str
class Array(Type):
      def __init__(self,type_obj,is_ptr=False,ptr_str=''):
            self.type_obj = type_obj
            self.is_ptr = is_ptr
            self.ptr_str = ptr_str
            if isinstance(type_obj,Type):
                  super().__init__(type_obj.type_name,type_obj.stdtype)
            elif isinstance(type_obj,Struct):
                  super().__init__(type_obj.name,type_obj.members)            
      
      def __str__(self):
            if isinstance(self.type_obj,Type):
                  return "std::vector<%s>%s" % (self.ptr_str,self.get_type_name())
            elif isinstance(self.type_obj,Struct):
                  return "std::vector<%s>%s" % (str(self.type_obj),self.ptr_str)

class Generic(Type):
      def __init__(self,name):
            super().__init__(name,False)

def is_compatible_ptr(type_a,type_b):
      if type_a.is_ptr == type_b.is_ptr:
            return True
      else:
            return False


def is_compatible_type(type_a,type_b):
      if type_a == type_b:
            return True
      
      if isinstance(type_a,Type) and isinstance(type_b,Type):
            if str(type_a.category) == str(type_b.category) and is_compatible_ptr(type_a,type_b):
                  return True
            else :
                  return False
      
      if isinstance(type_a,Struct) and isinstance(type_b,Struct):
            if str(type_a.category) == str(type_b.category) and is_compatible_ptr(type_a,type_b):
                  return True
            else :
                  return False

      return False