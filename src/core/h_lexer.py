# The Hascal Lexer
#
# The Hascal Programming Language
# Copyright 2019-2021 Hascal Development Team,
# all rights reserved.

from .sly import Lexer

class Lexer(Lexer):
        tokens = {
                NAME, FOR, WHILE, TO,DOWNTO,
                IF, ELSE,
                RETURN,
                INTVAR, STRINGVAR, CHARVAR,BOOLVAR,FLOATVAR,
                NUMBER, STRING,CHAR,
                GREATER, LESS, EQEQ, NOTEQ, GREATEREQ, LESSEQ,NOT,AND,OR,
                PLUS, TIMES, MINUS, DIVIDE,ALPHA,POW,
                DOT,
                ASSIGN,
                COMMA, COLON,
                LPAREN, RPAREN,
                LBC,RBC,
                LBRCK,RBRCK,
                TRUE,FALSE,
                VAR,CONST,
                SEM,
                USE,LOCAL,
                FUNCTION,
                BREAK,CONTINUE,
                STRUCT,ENUM}
        ignore = ' \t'
        ignore_comment_slash = r'#.*'
        
        NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
        NUMBER = r'\d+'

        PLUS   = r'\+'
        ALPHA = r'~'
        EQEQ   = r'=='
        MINUS  = r'-'
        TIMES  = r'\*'
        POW  = r'\^'
        DIVIDE = r'/'
        ASSIGN = r'='
        LPAREN = r'\('
        RPAREN = r'\)'
        LBC = r'\{'
        RBC = r'\}'
        SEM    = r';'
        COLON  = r':'
        COMMA = r','
        NOTEQ = r'!='
        LESSEQ = r'<='
        GREATEREQ = r'>='
        LESS = r'<'
        GREATER = r'>'
        LBRCK = r'\['
        RBRCK = r'\]'
        DOT = r'\.'
        
        NAME["var"] = VAR
        NAME["const"] = CONST
        
        NAME["use"] = USE
        NAME["local"] = LOCAL
        
        NAME["int"] = INTVAR
        NAME["string"] = STRINGVAR
        NAME["char"] = CHARVAR
        NAME["bool"] = BOOLVAR
        NAME["float"] = FLOATVAR
        
        NAME["not"] = NOT
        NAME["and"] = AND
        NAME["or"] = OR
        NAME["if"] = IF
        NAME["else"] = ELSE
        
        NAME["function"] = FUNCTION
        NAME["return"] = RETURN
        
        NAME["for"] = FOR
        NAME["to"] = TO
        NAME["downto"] = DOWNTO
        NAME["while"] = WHILE
        
        NAME["struct"] = STRUCT
        NAME["enum"] = ENUM
        
        NAME["true"] = TRUE
        NAME["false"] = FALSE
        
        NAME["break"] = BREAK
        NAME["continue"] = CONTINUE

        @_(r'"([^\n\\]|\\\S)*?"')
        def STRING(self, t):
                t.value = t.value[1:-1]
                return t
        @_(r'\'([^\n\\]|\\\S)*?\'')
        def CHAR(self, t):
                t.value = t.value[1:-1]
                return t
        @_(r'\n+')
        def newline(self, t):
                self.lineno += t.value.count('\n')

        def error(self, t):
                print("Illegal character '%s'" % t.value[0])
