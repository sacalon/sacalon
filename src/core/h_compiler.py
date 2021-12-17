# The Hascal Compiler
#
# The Hascal Programming Language
# Copyright 2019-2022 Hascal Development Team,
# all rights reserved.

from .h_error import HascalException
from .h_lexer import Lexer
from .h_parser import Parser
import sys
from os.path import isfile

class Generator(object):
      LDFLAGS = []
      def __init__(self,BASE_DIR):
            self.BASE_DIR = BASE_DIR
            self.src_includes = ""
            self.src_pre_main = ""
            #init standard types
            self.types = {
                  'int' : Type('int',True),
                  'float' : Type('float',True),
                  'bool' : Type('bool',True),
                  'char' : Type('char',True),
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

            }

            # list of imported libraries
            self.imported = []

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
                        HascalException(f"'{_name}' exists, cannot redefine it:{_line}")
                  elif _name in self.types :
                        HascalException(f"'{_name}' defined as a type, cannot redefine it as a variable:{_line}")
                  else:
                        members = {}

                        if isinstance(_type,Array):
                              _type_name = str(_type).split('<')[1].split('>')[0]
                              if _type_name in self.types and isinstance(self.types[_type_name],Struct) :
                                    members = self.types[_type_name].members
                        elif isinstance(_type,Struct) :
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
                  _type = node[2]
                  _line = node[4]

                  if _name in self.vars or _name in self.consts :
                        HascalException(f"'{_name}' exists ,cannot redefine it:{_line}")
                  elif _name in self.types :
                        HascalException(f"'{_name}' defined as a type ,cannot redefine it as a variable:{_line}")  
                  elif not _type in self.types :
                        HascalException(f"Type '{_type}' not defined:{_line}")
                  else:
                        members = {}
                        if isinstance(self.types[_type],Struct) : members = self.types[_type].members
                        self.vars[_name] = Var(_name,self.types[_type],members=members)
                        res =  "%s %s ;\n" % (_type,_name)

                        expr = {
                              'expr' : res,
                              'type' : self.types[_type],
                              'name' : _name,
                        }
                        return expr

            # var <name> : <return_type> = <expr>
            if node[0] == 'declare' and node[1] == "equal2":
                  _name = node[3]
                  _type = node[2]
                  _expr = self.walk(node[4])
                  _line = node[5]
            
                  if _name in self.vars or _name in self.consts  :
                        HascalException(f"'{_name}' exists ,cannot redefine it:{_line}")
                  elif _name in self.types :
                        HascalException(f"'{_name}' defined as a type ,cannot redefine it as a variable:{_line}")
                  elif str(_type) != str(_expr['type']) :
                        HascalException(f"Mismatched type {_type} and {_expr['type']}:{_line}")
                  elif not _type in self.types :
                        HascalException(f"Type '{_type}' not defined:{_line}")
                  else:
                        members = {}
                        if isinstance(self.types[_type],Struct) : members = self.types[_type].members
                        self.vars[_name] = Var(_name,self.types[_type],members=members)

                        expr = {
                              'expr' : "auto %s = %s;\n" % (_name,_expr['expr']),
                              'type' : self.types[_type],
                              'name' : _name,
                        }
                        return expr
                        
            # var <name> : [<return_type>]
            if node[0] == 'declare_array' and node[1] == "no_equal":
                  _name = node[3]
                  _type = node[2]
                  _line = node[4]

                  if _name in self.vars or _name in self.consts :
                        HascalException(f"'{_name}' exists ,cannot redefine it:{_line}")   
                  elif _name in self.types :
                        HascalException(f"'{_name}' defined as a type ,cannot redefine it as a variable:{_line}")   
                  elif not _type in self.types :
                        HascalException(f"Type '{_type}' not defined:{_line}")   
                  else:
                        members = {}
                        if isinstance(self.types[_type],Struct) : members = self.types[_type].members
                        self.vars[_name] = Var(_name,Array(self.types[_type]),is_array=True,members=members)
                        expr = {
                              'expr' : "std::vector<%s> %s;\n" % (_type,_name),
                              'type' : Array(self.types[_type]),
                              'name' : _name,
                        }
                        return expr

            # var <name> : [<return_type>] = <expr>
            if node[0] == 'declare_array' and node[1] == "equal2":
                  _name = node[3]
                  _type = node[2]
                  _expr = self.walk(node[4])
                  _line = node[5]

                  if _name in self.vars or _name in self.consts :
                        HascalException(f"'{_name}' exists ,cannot redefine it:{_line}")
                  elif _name in self.types :
                        HascalException(f"'{_name}' defined as a type ,cannot redefine it as a variable:{_line}")
                  elif str(Array(self.types[_type])) != str(_expr['type']) :
                        HascalException(f"Mismatched type {_type} and {_expr['type']}:{_line}")  
                  elif not _type in self.types :
                        HascalException(f"Type '{_type}' not defined:{_line}")  
                  else:
                        members = {}
                        if isinstance(self.types[_type],Struct) : members = self.types[_type].members
                        self.vars[_name] = Var(_name,Array(self.types[_type]),is_array=True,members=members)

                        expr = {
                              'expr' : "std::vector<%s> %s = %s ;\n" % (_type,_name,_expr['expr']),
                              'type' : Array(self.types[_type]),
                              'name' : _name,
                        }
                        return expr
                              
            # const <name> : <return_type> = <expr> ;
            if node[0] == 'declare' and node[1] == "const":
                  _name = node[3]
                  _type = node[2]
                  _expr = self.walk(node[4])
                  _line = node[5]

                  if _name in self.vars or _name in self.consts :
                        HascalException(f"'{_name}' exists ,cannot redefine it:{_line}")
                  elif _name in self.types :
                        HascalException(f"'{_name}' defined as a type ,cannot redefine it as a constant:{_line}")
                  elif str(_type) != str(_expr['type']) :
                        HascalException(f"Mismatched type {_type} and {_expr['type']}:{_line}")  
                  elif not _type in self.types :
                        HascalException(f"Type '{_type}' not defined:{_line}")
                  else:
                        self.consts[_name] = Const(_name,self.types[_type])
                        expr = {
                              'expr' : "const %s %s = %s ;\n" % (_type,_name,_expr['expr']),
                              'type' : self.types[_type],
                              'name' : _name,
                        }
                        return expr

            # const <name> = <expr> ;
            if node[0] == 'declare' and node[1] == "const":
                  _name = node[2]
                  _expr = self.walk(node[3])
                  _type = _expr['type']
                  _line = node[4]

                  if _name in self.vars or _name in self.consts :
                        HascalException(f"'{_name}' exists, cannot redefine it:{_line}")
                  elif _name in self.types :
                        HascalException(f"'{_name}' defined as a type, cannot redefine it as a constant:{_line}")   
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
                              HascalException(f"cannot found '{name}' library. Are you missing a library ?")
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
                              HascalException(f"cannot found '{name}' library. Are you missing a library ?")
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
                              HascalException(f"cannot found '{name}' library. Are you missing a library ?")
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
                              HascalException(f"cannot found '{name}' library. Are you missing a library ?")
                        if isfile(final_path_ld):
                              with open(final_path_ld) as f:
                                    ld = f.read().split(',')
                                    self.LDFLAGS += ld  

                  return {'expr':'','type':''}
            #-------------------------------------
            # <name> = <expr>   
            if node[0] == 'assign':
                  _name = node[1][0]
                  _expr = self.walk(node[2])
                  _line = node[3]

                  if len(node[1]) == 1:
                        if _name in self.consts :
                              HascalException(f"'{_name}'is a constant, cannot assign it")   
                        elif _name in self.types:
                              HascalException(f"'{_name}'is a type, cannot assign it")  
                        elif not _name in self.vars :
                              HascalException(f"Variable '{_name}' not defined")    
                        elif not isinstance(self.vars[_name].type,Struct) and (str(self.vars[_name].type) != str(_expr['type'])):
                              HascalException(f"Mismatched type {self.vars[_name].type} and {_expr['type']}:{_line}")    
                        else :
                              res = "%s = %s;\n" % (_name,_expr['expr'])
                              expr = {
                                    'expr' :  res,
                                    'type' : self.vars[_name].type,
                              }
                              return expr
                  else :                   
                        _full_name = '.'.join(arg for arg in node[1])

                        if _name in self.consts :
                              HascalException(f"'{_name}'is a constant, cannot assign it")  
                        elif _name in self.types:
                              HascalException(f"'{_name}'is a type, cannot assign it")   
                        elif not _name in self.vars :
                              HascalException(f"Variable '{_name}' not defined")

                        elif isinstance(self.types[str(self.vars[_name].type)],Struct) :
                              # if struct has no member show error else set current member to _current_member
                              if self.types[str(self.vars[_name].type)].members == {} :
                                    HascalException(f"Struct '{_name}' has no member:{_line}")
                              _members = self.types[str(self.vars[_name].type)].members

                              for i in range(len(node[1])):
                                    # check if node[1][i] is a member of struct and check it is not first member
                                    if node[1][i] in _members and i != 0 :
                                          _current_member = node[1][i]
                                          
                                          # check if current member is a struct
                                          if isinstance(_members[_current_member],Struct) :
                                                # if struct has no member show error else set _members to _members[_current_member]
                                                if _members[_current_member].members == {} :
                                                      HascalException(f"Struct '{_name}' has no member:{_line}")
                                                
                                                # check if current member is the last member of node[1]
                                                if i == len(node[1])-1 :
                                                      res = "%s = %s;\n" % (_full_name,_expr['expr'])
                                                      expr = {
                                                            'expr' :  res,
                                                            'type' : _members[_current_member],
                                                      }
                                                      
                                                      return expr
                                                _members = _members[_current_member].members
                                                continue
                                          else :
                                                _current_member = node[1][i]
                                                # check if current member exists
                                                if not _current_member in _members :
                                                      HascalException(f"Struct '{_name}' has no member:{_line}")
                                                
                                                # return expr
                                                expr = {
                                                      'expr' : "%s = %s;\n" % (_full_name,_expr['expr']),
                                                      'type' : _members[_current_member],
                                                }
                                                return expr
                                    elif i == 0 :
                                          continue
                                    else :
                                          HascalException(f"'{node[1][i]}' is not a member of '{_name}':{_line}")
                        else :
                              HascalException(f"Variable '{_name}' is not a struct:{_line}")

            # <name>[<expr>] = <expr>;
            if node[0] == 'assign_var_index':
                  _name = node[1][0]
                  _expr_index = self.walk(node[2])
                  _expr = self.walk(node[3])
                  _line = node[4]

                  if len(node[1]) == 1:
                        if _name in self.consts :
                              HascalException(f"'{_name}'is a constant, cannot assign it")   
                        elif _name in self.types:
                              HascalException(f"'{_name}'is a type, cannot assign it")  
                        elif not _name in self.vars :
                              HascalException(f"Variable '{_name}' not defined") 
                        elif not isinstance(self.vars[_name].type,Array):
                              HascalException(f"Variable '{_name}' is not subscriptable:{_line}")
                        elif self.vars[_name].type.type_name != str(_expr['type']):
                              HascalException(f"Mismatched3 type {self.vars[_name].type} and {_expr['type']}:{_line}") 
                        else :
                              if str(self.vars[_name].type).startswith('std::vector'):
                                    expr = {
                                          'expr' : "%s[%s] = %s;\n" % (_name,_expr_index['expr'],_expr['expr']),
                                          'type' : self.vars[_name].type.type_obj,
                                    }
                                    return expr
                              elif str(self.vars[_name].type) == 'string' :
                                    expr = {
                                          'expr' : "%s[%s] = %s;\n" % (_name,_expr_index['expr'],_expr['expr']),
                                          'type' : self.types['char'],
                                    }
                                    return expr
                              else :
                                    HascalException(f"Variable '{_name}' is not subscriptable:{_line}")
                  else :
                        _full_name = '.'.join(arg for arg in node[1])

                        if _name in self.consts :
                              HascalException(f"'{_name}'is a constant, cannot assign it")     
                        elif _name in self.types:
                              HascalException(f"'{_name}'is a type, cannot assign it")    
                        elif not _name in self.vars :
                              HascalException(f"Variable '{_name}' not defined")     

                        elif isinstance(self.types[str(self.vars[_name].type)],Struct) :
                              # if struct has no member show error else set current member to _current_member
                              if self.types[str(self.vars[_name].type)].members == {} :
                                    HascalException(f"Struct '{_name}' has no member:{_line}")
                              _members = self.types[str(self.vars[_name].type)].members

                              for i in range(len(node[1])):
                                    # check if node[1][i] is a member of struct and check it is not first member
                                    if node[1][i] in _members and i != 0 :
                                          _current_member = node[1][i]
                                          
                                          # check if current member is a struct
                                          if isinstance(_members[_current_member],Struct) :
                                                # if struct has no member show error else set _members to _members[_current_member]
                                                if _members[_current_member].members == {} :
                                                      HascalException(f"Struct '{_name}' has no member:{_line}")
                                                
                                                # check if current member is the last member of node[1]
                                                if i == len(node[1])-1 :
                                                      if not str(_members[_current_member]).startswith('std::vector'):
                                                            HascalException(f"'{_current_member}' is not an array:{_line}")
                                                      
                                                      if str(_members[_current_member]) == "string" :
                                                            expr = {
                                                                  'expr' :  "%s[%s] = %s;\n" % (_full_name,_expr_index['expr'],_expr['expr']),
                                                                  'type' : self.types['char'],
                                                            }
                                                            return expr
                                                      
                                                      expr = {
                                                            'expr' :  "%s[%s] = %s;\n" % (_full_name,_expr_index['expr'],_expr['expr']),
                                                            'type' : _members[_current_member],
                                                      }
                                                      return expr
                                                _members = _members[_current_member].members
                                                continue
                                          else :
                                                if not _current_member in _members :
                                                      HascalException(f"Struct '{_name}' has no member:{_line}")
                                                
                                                if i == len(node[1])-1 :
                                                      if not str(_members[_current_member]).startswith('std::vector'):
                                                                  HascalException(f"'{_current_member}' is not an array:{_line}")
                                                
                                                      expr = {
                                                            'expr' : "%s[%s] = %s;\n" % (_full_name,_expr_index['expr'],_expr['expr']),
                                                            'type' : _members[_current_member],
                                                      }
                                                      return expr
                                                else :
                                                      _members = self.types[_members[_current_member]].members
                                                      continue
                                    elif i == 0 :
                                          continue
                                    else :
                                          HascalException(f"'{node[1][i]}' is not a member of '{_name}':{_line}")     
                        else :
                              HascalException(f"Variable '{_name}' is not a struct:{_line}")
            
            # <name>[<expr>].<name> = <expr>;
            if node[0] == 'assign_var_index_struct':
                  _name = node[1][0]
                  _expr_index = self.walk(node[2])
                  _expr = self.walk(node[3])
                  _line = node[3]

                  if len(node[1]) == 1:
                        if _name in self.consts :
                              HascalException(f"'{_name}'is a constant, cannot assign it")   
                        elif _name in self.types:
                              HascalException(f"'{_name}'is a type, cannot assign it")  
                        elif not _name in self.vars :
                              HascalException(f"Variable '{_name}' not defined")    
                        elif _name in self.vars and (self.vars[_name].type != _expr['type']):
                              HascalException(f"Mismatched type {self.vars[_name].type} and {_expr['type']}:{_line}")
                        
                        else :
                              expr = {
                                    'expr' : "%s[%s] = %s;\n" % (_name,_expr_index['expr'],_expr['expr']),
                                    'type' : self.vars[_name].type,
                              }
                              return expr
                  else :
                        _full_name = '.'.join(arg for arg in node[1])
                        _first_name = node[1][0]
                        _end_name = node[1][len(node[1]-1)]
                        _final_type = None
                        if _name in self.consts :
                              HascalException(f"'{_name}'is a constant, cannot assign it")     
                        elif _name in self.types:
                              HascalException(f"'{_name}'is a type, cannot assign it")    
                        elif not _name in self.vars :
                              HascalException(f"Variable '{_name}' not defined")     
                        elif str(self.vars[_name].members[_end_name]) != _expr['type']:
                              HascalException(f"Mismatched type {str(self.vars[_name].members[_end_name])} and {_expr['type']}:{_line}")
                        elif isinstance(self.types[str(self.vars[_name].type)],Struct) :
                              # if struct has no member show error else set current member to _current_member
                              if self.types[str(self.vars[_name].type)].members == {} :
                                    HascalException(f"Struct '{_name}' has no member:{_line}")
                              _members = self.types[str(self.vars[_name].type)].members

                              for i in range(len(node[1])-1):
                                    # check if node[1][i] is a member of struct and check it is not first member
                                    if node[1][i] in _members and i != 0 :
                                          _current_member = node[1][i]
                                          
                                          # check if current member is a struct
                                          if isinstance(_members[_current_member],Struct) :
                                                # if struct has no member show error else set _members to _members[_current_member]
                                                if _members[_current_member].members == {} :
                                                      HascalException(f"Struct '{_name}' has no member:{_line}")
                                                
                                                # check if current member is the last member of node[1]
                                                if i == len(node[1])-1 :
                                                      # check if current member is an vector
                                                      if not _members[_current_member].type.startswith('std::vector') :
                                                            HascalException(f"Struct '{_name}' has no member:{_line}")
                                                      
                                                      if str(_members[_current_member]) == "string" :
                                                            expr = {
                                                                  'expr' :  "%s[%s] = %s;\n" % (_full_name,_expr_index['expr'],_expr['expr']),
                                                                  'type' : self.types['char'],
                                                            }
                                                            return expr

                                                      expr = {
                                                            'expr' :  "%s[%s] = %s;\n" % (_full_name,_expr_index['expr'],_expr['expr']),
                                                            'type' : _members[_current_member],
                                                      }
                                                      return expr
                                                _members = _members[_current_member].members
                                                continue
                                          else :
                                                if not _current_member in _members :
                                                      HascalException(f"Struct '{_name}' has no member:{_line}")
                                                if not _members[_current_member].type.startswith('std::vector') :
                                                            HascalException(f"Struct '{_name}' has no member:{_line}")

                                                expr = {
                                                      'expr' : "%s[%s] = %s;\n" % (_full_name,_expr_index['expr'],_expr['expr']),
                                                      'type' : _members[_current_member],
                                                }
                                                return expr
                                    elif i == 0 :
                                          continue
                                    else :
                                          HascalException(f"'{node[1][i]}' is not a member of '{_name}':{_line}")        
                        else :
                              HascalException(f"Variable '{_name}' is not a struct:{_line}")
            #-----------------------------------------
            # return <expr>
            if node[0] == 'return':
                  _expr = self.walk(node[1])
                  _line = node[2]

                  if _expr['expr'] in self.types :
                        HascalException(f"Cannot return a type '{_expr['expr']}':{_line}")
                  
                  expr = {
                        'expr' : "return %s;\n" %  _expr['expr'],
                        'type' : _expr['type']
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
                                    HascalException(f"cannot found '{name}' library. Are you missing a library ?")
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
                              except FileNotFoundError:
                                    HascalException(f"cannot found '{name}' library. Are you missing a library ?")            
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
                                    HascalException(f"cannot found '{name}' library. Are you missing a library ?")
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
                                          generator = Generator()
                                          output_cpp = generator.generate(tree,True)

                                          self.imported.append(name)
                                          self.imported += generator.imported
                                          self.add_to_output(output_cpp,generator.src_includes)
                                          self.funcs.update(generator.funcs)
                                          self.types.update(generator.types)
                              except FileNotFoundError:
                                    HascalException(f"cannot found '{name}' library. Are you missing a library ?")
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
                                    HascalException(f"cannot found '{name}' library. Are you missing a library ?")
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
                                          generator = Generator("./")
                                          output_cpp = generator.generate(tree,True)

                                          self.imported.append(name)
                                          self.imported += generator.imported
                                          self.add_to_output(output_cpp, generator.src_includes)
                                          self.funcs.update(generator.funcs)
                                          self.types.update(generator.types)
                              except FileNotFoundError:
                                    HascalException(f"cannot found '{name}' library. Are you missing a library ?")
                              
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
                                    HascalException(f"cannot found '{name}' library. Are you missing a library ?")

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
                                          generator = Generator("./")
                                          output_cpp = generator.generate(tree,True)

                                          self.imported.append(name)
                                          self.imported += generator.imported
                                          self.add_to_output(output_cpp, generator.src_includes)
                                          self.funcs.update(generator.funcs)
                                          self.types.update(generator.types)
                              except FileNotFoundError:
                                    HascalException(f"cannot found '{name}' library. Are you missing a library ?")
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
                  _name = node[2]
                  _return_type = node[1]
                  _params = { }

                  params = node[3].split(',')
                  if len(params) != 1:
                        for p in params:
                              param = p.split(' ')
                              _params[param[1]] = param[0]
                              if param[0].endswith(']'): self.vars[param[1]] = Var(param[1],param[0],is_array=True)
                              else : self.vars[param[1]] = Var(param[1],param[0])
                  elif len(params) == 1 and params[0] != '' and params[0] != None: 
                        param = params[0].split(' ')
                        _params[param[1]] = param[0]
                        self.vars[param[1]] = Var(param[1],param[0])
                  
                  if self.funcs.get(_name) != None:
                        self.funcs[_name] = [self.funcs[_name],Function(_name,_params,_return_type)]
                  else :
                        self.funcs[_name] = Function(_name,_params,_return_type)

                  _name = node[2]
                  _compiled_params = node[3]
                  _expr = self.walk(node[4])
                  _res = ""
                  for e in _expr :
                        _res += e['expr']
                  res = "%s %s(%s) {\n%s\n}\n" % (_return_type,_name,_compiled_params,_res) 

                  # program arguments 
                  _params_keys = list(_params.keys())
                  if not _compiled_params in ['',None] and (_name == "main" and _params[_params_keys[0]] == "std::vector<string>"):
                        res = "%s %s(int argc,char** args) {\nstd::vector<std::string> argv;\nif (argc > 1) {argv.assign(args + 1, args + argc);}\nelse {argv = { args[0] };}\n%s\n}\n" % (_return_type,_name,_res) 
                        expr = {
                              'expr' : res,
                              'type' : _return_type,
                        }
                        return expr
                  self.vars = current_vars
                  
                  expr = {
                        'expr' : res,
                        'type' : _return_type,
                  }
                  return expr
            #-------------------------------------
            if node[0] == "inline_function" :
                  _name = node[2]
                  _return_type = node[1]
                  _params = { }

                  params = node[3].split(',')
                  if len(params) != 1:
                        for p in params:
                              param = p.split(' ')
                              _params[param[1]] = param[0]
                  elif len(params) == 1 and (params[0] != '' and params[0] != None) : 
                        param = params[0].split(' ')
                        _params[param[1]] = param[0]
                  
                  if self.funcs.get(_name) != None:
                        self.funcs[_name] = [self.funcs[_name],Function(_name,_params,_return_type)]
                  else :
                        self.funcs[_name] = Function(_name,_params,_return_type)

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
                              HascalException(f"Incomplete type definition '{_name}':{_line}")
                        
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
                        HascalException(f"Cannot found struct '{_i_name}'")

                  # generate output code and member
                  res = ""
                  for e in _body :
                        if str(e['type']) == _name :
                              HascalException(f"Incomplete type definition '{_name}':{_line}")
                        
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
                        res += e['expr']

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
                        HascalException(f"'{_name2}' not defined:{_line}") #todo

                  if not isinstance(self.vars[_name2].type,Array) :
                        HascalException(f"'{_name2}' is not iterable:{_line}") 

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
                                                            HascalException(f"{_name} has more parameters than given:{_line}")
                                                      else :
                                                            HascalException(f"{_name} has less parameters than given:{_line}")
                                                else :
                                                      counter += 1
                                                      continue
                                          else :
                                                expr = {
                                                      'expr' : '%s(%s)' % (f.name,','.join(self.walk(arg)['expr'] for arg in node[2])),
                                                      'type' : f.return_type,
                                                }
                                                return expr
                                          counter += 1
                              if _name in self.types:
                                    if not isinstance(self.types[_name],Struct):
                                          HascalException(f"Cannot call type {_name}:{_line}")
                                    
                                    expr = {
                                          'expr' : "%s{%s}" % (_name, ', '.join(self.walk(arg)['expr'] for arg in node[2])),
                                          'type' : self.types[_name],
                                    }
                                    return expr
                              else :
                                    expr = {
                                          'expr' : "%s(%s)" % (_name, ', '.join(self.walk(arg)['expr'] for arg in node[2])),
                                          'type' : self.funcs[_name].return_type,
                                    }
                                    return expr
                  else :
                        HascalException(f"Function '{_name}' not defined")
            # --------------operators-----------------
            # todo : error if string *-/ string
            # <expr> + <expr>
            if node[0] == 'add':
                  _expr0 = self.walk(node[1])
                  _expr1 = self.walk(node[2])
                  _line = node[3]
                  if str(_expr0['type']) != str(_expr1['type']) :
                        HascalException(f"Mismatched type {_expr0['type']} and {_expr1['type']}:{_line}")
                        
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
                        HascalException(f"Mismatched type {_expr0['type']} and {_expr1['type']}:{_line}.")  
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
                        HascalException(f"Mismatched type {_expr0['type']} and {_expr1['type']}:{_line}") 
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
                        HascalException(f"Mismatched type {_expr0['type']} and {_expr1['type']}:{_line}") 
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
                        HascalException(f"Mismatched type {_expr0['type']} and {_expr1['type']}:{_line}")
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
                        HascalException(f"Mismatched type {_expr0['type']} and {_expr1['type']}:{_line}")
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
                        HascalException(f"Mismatched type {_expr0['type']} and {_expr1['type']}:{_line}")
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
                        HascalException(f"Mismatched type {_expr0['type']} and {_expr1['type']}:{_line}")
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
                        HascalException(f"Mismatched type {_expr0['type']} and {_expr1['type']}:{_line}")
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
                        HascalException(f"Mismatched type {_expr0['type']} and {_expr1['type']}:{_line}")
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
                        'expr' : '!%s' % (_expr['expr']), # may have bug
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
                              HascalException(f"'{_name}' is not reachable or not defined:{_line}")
                  else :
                        _full_name = '.'.join(arg for arg in node[1])

                        if _name in self.vars:
                              if isinstance(self.types[str(self.vars[_name].type)],Struct) :
                                    # if struct has no member show error else set current member to _current_member
                                    if self.types[str(self.vars[_name].type)].members == {} :
                                          HascalException(f"Struct '{_name}' has no member:{_line}")
                                    _members = self.types[str(self.vars[_name].type)].members

                                    for i in range(len(node[1])):
                                          # check if node[1][i] is a member of struct and check it is not first member
                                          if node[1][i] in _members and i != 0 :
                                                _current_member = node[1][i]

                                                # check if current member is a struct
                                                if isinstance(_members[_current_member],Struct) :
                                                      # if struct has no member show error else set _members to _members[_current_member]
                                                      if _members[_current_member].members == {} :
                                                            HascalException(f"Struct '{_name}' has no member:{_line}")
                                                
                                                      # check if current member is the last member of node[1]
                                                      if i == len(node[1])-1 :
                                                            # check if current member is an vector
                                                            if not _members[_current_member].type.startswith('std::vector') :
                                                                  HascalException(f"Struct '{_name}' has no member:{_line}")
                                                            expr = {
                                                                  'expr' :  "%s" % (_full_name),
                                                                  'type' : _members[_current_member],
                                                            }
                                                            return expr
                                                      _members = _members[_current_member].members
                                                      continue
                                                else :
                                                      if not _current_member in _members :
                                                            HascalException(f"Struct '{_name}' has no member:{_line}")
                                                      if str(_members[_current_member]).startswith('std::vector') :
                                                            expr = {
                                                                  'expr' : "%s" % (_full_name),
                                                                  'type' : self.types[str(_members[_current_member]).split('<')[1].split('>')[0]],
                                                            }
                                                            return expr  

                                                      expr = {
                                                            'expr' : "%s" % (_full_name),
                                                            'type' : _members[_current_member],
                                                      }
                                                      return expr
                                          elif i == 0 :    
                                                continue
                                          else :
                                                HascalException(f"'{node[1][i]}' is not a member of '{_name}':{_line}")  

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
                                          HascalException(f"Struct '{_name}' has no member:{_line}")
                                    _members = self.types[self.consts[_name].type].members

                                    for i in range(len(node[1])-1):
                                          # check if node[1][i] is a member of struct and check it is not first member
                                          if node[1][i] in _members and i != 0 :
                                                _current_member = node[1][i]
                                          
                                                # check if current member is a struct
                                                if isinstance(_members[_current_member],Struct) :
                                                      # if struct has no member show error else set _members to _members[_current_member]
                                                      if _members[_current_member].members == {} :
                                                            HascalException(f"Struct '{_name}' has no member:{_line}")
                                                
                                                      # check if current member is the last member of node[1]
                                                      if i == len(node[1])-1 :
                                                            # check if current member is an vector
                                                            if not _members[_current_member].type.startswith('std::vector') :
                                                                  HascalException(f"Struct '{_name}' has no member:{_line}")

                                                            expr = {
                                                                  'expr' :  "%s" % (_full_name),
                                                                  'type' : _members[_current_member],
                                                            }
                                                            return expr
                                                      _members = _members[_current_member].members
                                                      continue
                                                else :
                                                      if not _current_member in _members :
                                                            HascalException(f"Struct '{_name}' has no member:{_line}")
                                                      if not _members[_current_member].type.startswith('std::vector') :
                                                                  HascalException(f"Struct '{_name}' has no member:{_line}")

                                                      expr = {
                                                            'expr' : "%s" % (_full_name),
                                                            'type' : _members[_current_member],
                                                      }
                                                      return expr
                                          elif i == 0 : ...
                                          else :
                                                HascalException(f"'{node[1][i]}' is not a member of '{_name}':{_line}")  

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
                              HascalException(f"'{_name}' is not reachable or not defined:{_line}")                             
            #---------------------------------------
            # <name>[<expr>]
            if node[0] == 'var_index':
                  _name = node[1][0]
                  _expr = self.walk(node[2])
                  _line = node[3]
                  if len(node[1]) == 1:
                        if _name in self.vars:
                              if str(self.vars[_name].type).startswith('std::vector'):
                                    expr = {
                                          'expr' : "%s[%s]" % (_name,_expr['expr']),
                                          'type' : self.types[str(self.vars[_name].type).split('<')[1].split('>')[0]],
                                    }
                                    return expr
                              elif not str(self.vars[_name].type).startswith('string'):
                                    HascalException(f"{_name} is not subscriptable:{_line}")
                              
                              expr = {
                                    'expr' : "%s[%s]" % (_name,_expr['expr']),
                                    'type' : self.vars[_name].type,
                              }
                              return expr
                        elif _name in self.consts :
                              if str(self.consts[_name].type).startswith('std::vector'):
                                    expr = {
                                          'expr' : "%s[%s]" % (_name,_expr['expr']),
                                          'type' : self.types[str(self.vars[_name].type).split('<')[1].split('>')[0]],
                                    }
                                    return expr
                              elif not str(self.vars[_name].type).startswith('string'):
                                    HascalException(f"{_name} is not subscriptable:{_line}")

                              expr = {
                                    'expr' : "%s" % (_name,_expr['expr']),
                                    'type' : self.consts[_name].type,
                              }
                              return expr
                        else :
                              HascalException(f"'{_name}' is not reachable or not defined:{_line}")
                  else :
                        _end_name = node[1][len(node[1])-1]
                        _full_name = '.'.join(arg for arg in node[1])
                        if _name in self.vars: 
                              if str(self.vars[_name].type).startswith('std::vector'):
                                    expr = {
                                          'expr' : "%s[%s]" % (_name,_expr['expr']),
                                          'type' : self.types[str(self.vars[_name].type).split('<')[1].split('>')[0]],
                                    }
                                    return expr  
                              elif not str(self.vars[_name].type).startswith('string'):
                                    HascalException(f"{_name} is not subscriptable:{_line}")

                              expr = {
                                    'expr' : "%s" % (_full_name,_expr['expr']),
                                    'type' : self.vars[_name].type,
                              }
                              return expr
                        elif _name in self.consts :
                              if str(self.consts[_name].type).startswith('std::vector'):
                                    expr = {
                                          'expr' : "%s[%s]" % (_name,_expr['expr']),
                                          'type' : self.types[str(self.vars[_name].type).split('<')[1].split('>')[0]],
                                    }
                                    return expr  
                              elif not str(self.vars[_name].type).startswith('string'):
                                    HascalException(f"{_name} is not subscriptable:{_line}")

                              expr = {
                                    'expr' : "%s" % (_full_name,_expr['expr']),
                                    'type' : self.consts[_name].type,
                              }
                              return expr
                        else :
                              HascalException(f"'{_name}' is not reachable or not defined:{_line}")
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
            if node[0] == 'string':
                  expr = {
                        'expr' : 'std::string(R"(%s)")' % node[1],
                        'type' : self.types[node[0]],
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
      def __init__(self,name,members):
            self.name = name
            self.members = members
            self.stdtype = False
      def __str__(self):
            return self.name

class Enum(Struct):
      ...

class Type(object):
      def __init__(self,type_name,stdtype):
            self.type_name = type_name
            self.stdtype = stdtype
      def __str__(self):
            return "%s" % (self.type_name)

class Array(Type):
      def __init__(self,type_obj):
            self.type_obj = type_obj
            if isinstance(type_obj,Type):
                  super().__init__(type_obj.type_name,type_obj.stdtype)
            elif isinstance(type_obj,Struct):
                  super().__init__(type_obj.name,type_obj.members)            
      
      def __str__(self):
            if isinstance(self.type_obj,Type):
                  return "std::vector<%s>" % (self.type_name)
            elif isinstance(self.type_obj,Struct):
                  return "std::vector<%s>" % (self.type_obj.name)
            