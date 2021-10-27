# The Hascal Parser
# 
# The Hascal Programming Language
# Copyright 2019-2022 Hascal Development Team,
# all rights reserved.

from .sly import Parser
from .h_lexer import Lexer

class Parser(Parser):
      tokens = Lexer.tokens
      precedence = (
            ('left', PLUS, MINUS),
            ('left', TIMES, DIVIDE),
            ('right', UMINUS)
            )

      def __init__(self):
            ...

      @_('')
      def block(self, p):
            return ('block', )
      @_('statement block')
      def block(self, p):
            return ('block', p.statement, *p.block[1:])
      
      @_('')
      def in_block(self, p):
            return ('in_block', )
      @_('in_statement in_block')
      def in_block(self, p):
            return ('in_block', p.in_statement, *p.in_block[1:])
      #----------------------------------
      @_('')
      def block_struct(self, p):
            return ('block_struct', )
      @_('struct_declare block_struct')
      def block_struct(self, p):
            return ('block_struct', p.struct_declare, *p.block_struct[1:])

      @_('VAR NAME ASSIGN expr')
      def struct_declare(self, p):
            return ('declare','equal1','auto', p.NAME, p.expr)
      @_('CONST NAME ASSIGN expr')
      def struct_declare(self, p):
            return ('declare','const', p.NAME, p.expr)
            
      @_('VAR NAME COLON return_type')
      def struct_declare(self, p):
            return ('declare','no_equal',p.return_type, p.NAME) 
      @_('VAR NAME COLON return_type ASSIGN expr')
      def struct_declare(self, p):
            return ('declare','equal2',p.return_type, p.NAME,p.expr) 
            
      @_('VAR NAME COLON LBRCK return_type RBRCK')
      def struct_declare(self, p):
            return ('declare_array','no_equal',p.return_type, p.NAME) 
            
      @_('VAR NAME COLON LBRCK return_type RBRCK ASSIGN expr')
      def struct_declare(self, p):
            return ('declare_array','equal2',p.return_type, p.NAME,p.expr)
      #-----------------------------------
      # use <name>
      @_('USE name')
      def statement(self, p):
            return ('use', p.name)
      
      # local use <name>
      @_('LOCAL USE name')
      def statement(self, p):
            return ('use_local', p.name)
      #-----------------------------------
      @_('enum_stmt')
      def statement(self, p):
            return p.enum_stmt
      @_('enum_stmt')
      def in_statement(self, p):
            return p.enum_stmt
      # enum <name> {
      #     <names>     
      # }
      @_('ENUM NAME LBC names RBC')
      def enum_stmt(self, p):
            return ('enum', p.NAME,p.names)
      #----------------------------------
      # statement : 
      @_('var_declare')
      def statement(self, p):
            return p.var_declare

      # var <name> : <return_type>
      @_('VAR NAME COLON return_type')
      def var_declare(self, p):
            return ('declare','no_equal',p.return_type, p.NAME) 

      # var <name> : [<return_type>]
      @_('VAR NAME COLON LBRCK return_type RBRCK')
      def var_declare(self, p):
            return ('declare_array','no_equal',p.return_type, p.NAME) 

      # var <name> = <expr>
      @_('VAR NAME ASSIGN expr')
      def var_declare(self, p):
            return ('declare','equal1','auto', p.NAME, p.expr)

      # var <name> : <return_type> = <expr>
      @_('VAR NAME COLON return_type ASSIGN expr')
      def var_declare(self, p):
            return ('declare','equal2',p.return_type, p.NAME,p.expr) 
            
      # var <name> : [<return_type>] = <expr>
      @_('VAR NAME COLON LBRCK return_type RBRCK ASSIGN expr')
      def var_declare(self, p):
            return ('declare_array','equal2',p.return_type, p.NAME,p.expr) 

      # const <name> = <expr>
      @_('CONST NAME ASSIGN expr')
      def var_declare(self, p):
            return ('declare','const', p.NAME, p.expr)
      
      # const <name> : <return_type> = <expr>
      @_('CONST NAME COLON return_type ASSIGN expr')
      def var_declare(self, p):
            return ('declare','const_type',p.return_type, p.NAME, p.expr)

      # in_statement : 
      @_('in_var_declare')
      def in_statement(self, p):
            return p.in_var_declare

      # in : var <name> : <return_type>
      @_('VAR NAME COLON return_type')
      def in_var_declare(self, p):
            return ('in_declare','no_equal',p.return_type, p.NAME) 

      # in : var <name> : [<return_type>]
      @_('VAR NAME COLON LBRCK return_type RBRCK')
      def in_var_declare(self, p):
            return ('in_declare_array','no_equal',p.return_type, p.NAME) 

      # in : var <name> = <expr>
      @_('VAR NAME ASSIGN expr')
      def in_var_declare(self, p):
            return ('in_declare','equal1','auto', p.NAME, p.expr)

      # in : var <name> : <return_type> = <expr>
      @_('VAR NAME COLON return_type ASSIGN expr')
      def in_var_declare(self, p):
            return ('in_declare','equal2',p.return_type, p.NAME,p.expr) 
            
      # in : var <name> : [<return_type>] = <expr>
      @_('VAR NAME COLON LBRCK return_type RBRCK ASSIGN expr')
      def in_var_declare(self, p):
            return ('in_declare_array','equal2',p.return_type, p.NAME,p.expr) 

      # in : const <name> = <expr>
      @_('CONST NAME ASSIGN expr')
      def in_var_declare(self, p):
            return ('in_declare','const', p.NAME, p.expr)
      
      # in : const <name> : <return_type> = <expr>
      @_('CONST NAME COLON return_type ASSIGN expr')
      def in_var_declare(self, p):
            return ('in_declare','const_type',p.return_type, p.NAME, p.expr)
      #-----------------------------------
      # <name> = <expr>
      @_('name ASSIGN expr')
      def in_statement(self, p):
            return ('assign', p.name, p.expr)
      
      # <name>[<expr>] = <expr>
      @_('name LBRCK expr RBRCK ASSIGN expr')
      def in_statement(self, p):
            return ('assign_var_index', p.name,p.expr0,p.expr1)
      #-----------------------------------
      @_('if_stmt')
      def in_statement(self, p):
            return p.if_stmt

      # if <condition> {
      #      <block>
      # }
      @_('IF condition LBC block RBC')
      def if_stmt(self, p):
            return ('if', p.condition,p.block)

      # if <condition> {
      #      <block>
      # } else {
      #      <block>
      # }
      @_('IF condition LBC block RBC ELSE LBC block RBC')
      def if_stmt(self, p):
            return ('if_else', p.condition,p.block0,p.block1)
      
      # if <condition> {
      #      <block>
      # } else <condition> {
      #      <block>
      # }
      @_('IF condition LBC block RBC ELSE if_stmt')
      def if_stmt(self, p):
            return ('if_else2', p.condition,p.block,p.if_stmt)
      #-----------------------------------
      # return <expr>
      @_('RETURN expr')
      def in_statement(self, p):
            return ('return', p.expr)
      #-----------------------------------
      @_('for_stmt')
      def in_statement(self, p):
            return p.for_stmt
      # for <name> = <expr> to <expr> {
      #      <block>
      # }
      @_('FOR NAME ASSIGN expr TO expr LBC block RBC')
      def for_stmt(self, p):
            return ('for', p.NAME,p.expr0,p.expr1,p.block)

      # for <name> = <expr> downto <expr> {
      #      <block>
      # }
      @_('FOR NAME ASSIGN expr DOWNTO expr LBC block RBC')
      def for_stmt(self, p):
            return ('for_down', p.NAME,p.expr0,p.expr1,p.block)
      #-----------------------------------
      @_('while_stmt')
      def in_statement(self, p):
            return p.while_stmt
      # while <condition> {
      #      <block>
      # }
      @_('WHILE condition LBC block RBC')
      def while_stmt(self, p):
            return ('while',p.condition,p.block)
      #-----------------------------------
      @_('struct_stmt')
      def statement(self, p):
            return p.struct_stmt
      # struct <name> {
      #     <block_struct>
      # }
      @_('STRUCT NAME LBC block_struct RBC')
      def struct_stmt(self, p):
            return ('struct',p.NAME,p.block_struct)
      #-----------------------------------
      # break
      @_('BREAK')
      def in_statement(self, p):
            return ('break')
      
      # continue
      @_('CONTINUE')
      def in_statement(self, p):
            return ('continue')
      #-----------------------------------
      # function <name> {
      #      <in_block>
      # }
      @_('FUNCTION NAME LBC in_block RBC')
      def statement(self, p):
            return ('function','void', p.NAME, "", p.in_block)

      # function <name>() {
      #      <in_block>
      # }
      @_('FUNCTION NAME LPAREN RPAREN LBC in_block RBC')
      def statement(self, p):
            return ('function','void', p.NAME,"", p.in_block)

      # function <name>(<params>) {
      #      <in_block>
      # }
      @_('FUNCTION NAME LPAREN params RPAREN LBC in_block RBC')
      def statement(self, p):
            return ('function','void', p.NAME, p.params, p.in_block)
 
      # function <name> : <return_type> {
      #      <in_block>
      # }   
      @_('FUNCTION NAME COLON return_type LBC in_block RBC')
      def statement(self, p):
            return ('function',p.return_type, p.NAME, "", p.in_block)

      # function <name>() : <return_type> {
      #      <in_block>
      # } 
      @_('FUNCTION NAME LPAREN RPAREN COLON return_type LBC in_block RBC')
      def statement(self, p):
            return ('function',p.return_type, p.NAME, "", p.in_block) 

      # function <name>(<params>) : <return_type> {
      #      <in_block>
      # }  
      @_('FUNCTION NAME LPAREN params RPAREN COLON return_type LBC in_block RBC')
      def statement(self, p):
            return ('function',p.return_type, p.NAME, p.params, p.in_block)
      
      # function <name> : [<return_type>] {
      #      <in_block>
      # }
      @_('FUNCTION NAME COLON return_type2 LBC in_block RBC')
      def statement(self, p):
            return ('function',p.return_type2, p.NAME, "", p.in_block)
      
      
      # function <name>() : [<return_type>] {
      #      <in_block>
      # }
      @_('FUNCTION NAME LPAREN COLON return_type2 RPAREN LBC in_block RBC')
      def statement(self, p):
            return ('function',p.return_type2, p.NAME,"", p.in_block)

      # function <name>(<params>) : [<return_type>] {
      #      <in_block>
      # }
      @_('FUNCTION NAME LPAREN params RPAREN COLON return_type2 LBC in_block RBC')
      def statement(self, p):
            return ('function',p.return_type2, p.NAME, p.params, p.in_block)    

      # function <name>(<params>) : <return_type>
      @_('FUNCTION NAME LPAREN params RPAREN COLON return_type')
      def statement(self, p):
            return ('inline_function',p.return_type, p.NAME, p.params)  
      # function <name>() : <return_type>
      @_('FUNCTION NAME LPAREN RPAREN COLON return_type')
      def statement(self, p):
            return ('inline_function',p.return_type, p.NAME)  
      #------------------------------------
      @_('expr')
      def in_statement(self, p):
            return ('expr', p.expr)
      
      @_('expr')
      def exprs(self, p):
            return p.expr
      @_('exprs COMMA expr')
      def exprs(self, p):
            return ('exprs', p.exprs, p.expr)
      @_('LBRCK exprs RBRCK')
      def expr(self, p):
            return ('list', p.exprs)
            
      @_('expr PLUS expr')
      def expr(self, p):
            return ('add', p.expr0, p.expr1)
      
      @_('expr TIMES expr')
      def expr(self, p):
            return ('mul', p.expr0, p.expr1)
      @_('expr MINUS expr')
      def expr(self, p):
            return ('sub', p.expr0, p.expr1)
      @_('expr DIVIDE expr')
      def expr(self, p):
            return ('div', p.expr0, p.expr1)
      @_('expr POW expr')
      def expr(self, p):
            return ('pow', p.expr0, p.expr1)
      @_('MINUS expr %prec UMINUS')
      def expr(self, p):
            return ('sub', ('number', 0), p.expr)
      @_('expr ALPHA expr')
      def expr(self, p):
            return ('add_cont', p.expr0, p.expr1)
      @_('LPAREN expr RPAREN')
      def expr(self, p):
            return ('paren_expr',p.expr)

      @_('NAME LPAREN args RPAREN')
      def expr(self, p):
            return ('call', p.NAME, p.args)
      @_('NAME LPAREN RPAREN')
      def expr(self, p):
            return ('call', p.NAME, ())
      @_('name')
      def expr(self, p):
            return ('var', p.name)
      @_('NOT expr')
      def expr(self, p):
            return ('not', p.expr)
      @_('name LBRCK expr RBRCK')
      def expr(self, p):
            return ('var_index', p.name,p.expr)
      @_('NUMBER')
      def expr(self, p):
            return ('number', p.NUMBER)
      @_('STRING')
      def expr(self, p):
            return ('string', p.STRING)
      @_('CHAR')
      def expr(self, p):
            return ('char', p.CHAR)
      @_('boolean')
      def expr(self, p):
            return ('bool', p.boolean)
      @_('float')
      def expr(self, p):
            return ('float', p.float)
      @_('expr DOT NAME')
      def expr(self, p):
            return ('.', p.expr,p.NAME)
      @_('expr DOT name LBRCK expr RBRCK')
      def expr(self, p):
            return ('.2', p.expr0,p.name,p.expr1)
      @_('NUMBER DOT NUMBER')
      def float(self, p):
            return "{0}.{1}".format(p.NUMBER0,p.NUMBER1)
      @_('name_t')
      def name(self, p):
            return [p.name_t]
      @_('name DOT name_t')
      def name(self, p):
            return p.name + [p.name_t]
    
      @_('NAME')
      def name_t(self, p):
            return p.NAME
            
      @_('TRUE')
      def boolean(self, p):
            return 'true'
      @_('FALSE')
      def boolean(self, p):
            return 'false'
            
      #------------------------------------------
      @_('names COMMA NAME')
      def names(self, p):
            return "{0},{1}".format(p.names,p.NAME)
      @_('NAME')
      def names(self, p):
            return p.NAME
      #------------------------------------------
      @_('expr EQEQ expr')
      def condition(self, p):
            return ('equals', p.expr0, p.expr1)
      @_('expr NOTEQ expr')
      def condition(self, p):
            return ('not_equals', p.expr0, p.expr1)
      @_('expr GREATEREQ expr')
      def condition(self, p):
            return ('greater_equals', p.expr0, p.expr1)
      @_('expr LESSEQ expr')
      def condition(self, p):
            return ('less_equals', p.expr0, p.expr1)
      @_('expr GREATER expr')
      def condition(self, p):
            return ('greater', p.expr0, p.expr1)
      @_('expr LESS expr')
      def condition(self, p):
            return ('less', p.expr0, p.expr1)
      
      @_('NOT condition')
      def condition(self, p):
            return ('not_cond', p.condition)
      @_('boolean')
      def condition(self, p):
            return ('bool_cond', p.boolean)

      @_('condition AND condition')
      def condition(self, p):
            return ('and', p.condition0,p.condition1)
      @_('condition OR condition')
      def condition(self, p):
            return ('or', p.condition0,p.condition1)
      #-----------------------------------------
      @_('param_t')
      def params(self, p):
            return str(p.param_t)
      @_('params COMMA param_t')
      def params(self, p):
            return str(p.params + "," + p.param_t)

      @_('NAME COLON return_type')
      def param_t(self, p):
            return "{0} {1}".format(p.return_type,p.NAME)
      @_('NAME COLON return_type2')
      def param_t(self, p):
            return "{0} {1}".format(p.return_type2,p.NAME)
      #------------------------------------------
      @_('arg')
      def args(self, p):
            return [p.arg]
      @_('args COMMA arg')
      def args(self, p):
            return p.args + [p.arg]

      @_('expr')
      def arg(self, p):
            return p.expr
      #------------------------------------------
      @_('INTVAR')
      def return_type(self, p):
            return 'int'
      @_('STRINGVAR')
      def return_type(self, p):
            return 'string'
      @_('CHARVAR')
      def return_type(self, p):
            return 'char'
      @_('BOOLVAR')
      def return_type(self, p):
            return 'bool'
      @_('FLOATVAR')
      def return_type(self, p):
            return 'float'
      @_('NAME')
      def return_type(self, p):
            return str(p.NAME)
            
      @_('LBRCK INTVAR RBRCK')
      def return_type2(self, p):
            return 'int[]'
      @_('LBRCK STRINGVAR RBRCK')
      def return_type2(self, p):
            return 'string[]'
      @_('LBRCK CHARVAR RBRCK')
      def return_type2(self, p):
            return 'char[]'
      @_('LBRCK BOOLVAR RBRCK')
      def return_type2(self, p):
            return 'bool[]'
      @_('LBRCK FLOATVAR RBRCK')
      def return_type2(self, p):
            return 'float[]'
      @_('LBRCK NAME RBRCK')
      def return_type2(self, p):
            return "{0}[]".format(p.NAME)
      #------------------------------------------