from .sly import Lexer
from .h_error import HascalError
from sys import exit


class Lexer(Lexer):
    tokens = {
        NAME,
        FOR,
        WHILE,
        IN,
        IF,
        ELSE,
        RETURN,
        INTVAR,
        STRINGVAR,
        CHARVAR,
        BOOLVAR,
        FLOATVAR,
        VOIDVAR,
        STATIC,
        NUMBER,
        STRING,
        CHAR,
        MULTILINE_STRING,
        GREATER,
        LESS,
        EQEQ,
        NOTEQ,
        GREATEREQ,
        LESSEQ,
        NOT,
        AND,
        OR,
        PLUS,
        TIMES,
        MINUS,
        DIVIDE,
        POW,
        DOT,
        ASSIGN,
        COMMA,
        COLON,
        LPAREN,
        RPAREN,
        LBC,
        RBC,
        LBRCK,
        RBRCK,
        TRUE,
        FALSE,
        VAR,
        CONST,
        USE,
        FUNCTION, FUNCTION_TYPE,
        BREAK,
        CONTINUE,
        CUSE,
        STRUCT,
        ENUM,
        AMP,
        QS,
        NEW,
        DELETE,
        AT,
    }
    ignore = " \t"
    ignore_comment_slash = r"//.*"
    ignore_multiline_comment_slash = r"\/\*((?!\*\/)[^\r\n])*[\r\n]((?!\*\/)[\s\S\r\n])*\*\/"

    NAME = r"\w+"
    NUMBER = r"\d+"

    PLUS = r"\+"
    EQEQ = r"=="
    MINUS = r"-"
    TIMES = r"\*"
    POW = r"\^"
    DIVIDE = r"/"
    ASSIGN = r"="
    LPAREN = r"\("
    RPAREN = r"\)"
    LBC = r"\{"
    RBC = r"\}"
    COLON = r":"
    COMMA = r","
    NOTEQ = r"!="
    LESSEQ = r"<="
    GREATEREQ = r">="
    LESS = r"<"
    GREATER = r">"
    LBRCK = r"\["
    RBRCK = r"\]"
    DOT = r"\."
    AMP = r"&"
    AT = r"@"
    QS = r"\?"

    NAME["var"] = VAR
    NAME["const"] = CONST

    NAME["use"] = USE
    NAME["cuse"] = CUSE

    NAME["int"] = INTVAR
    NAME["string"] = STRINGVAR
    NAME["char"] = CHARVAR
    NAME["bool"] = BOOLVAR
    NAME["float"] = FLOATVAR
    NAME["void"] = VOIDVAR
    NAME["Function"] = FUNCTION_TYPE
    NAME["static"] = STATIC

    NAME["not"] = NOT
    NAME["and"] = AND
    NAME["or"] = OR
    NAME["if"] = IF
    NAME["else"] = ELSE

    NAME["function"] = FUNCTION
    NAME["return"] = RETURN

    NAME["for"] = FOR
    NAME["in"] = IN
    NAME["while"] = WHILE

    NAME["struct"] = STRUCT
    NAME["enum"] = ENUM

    NAME["true"] = TRUE
    NAME["false"] = FALSE

    NAME["break"] = BREAK
    NAME["continue"] = CONTINUE

    NAME["new"] = NEW
    NAME["delete"] = DELETE

    @_(r'("(?!"").*?(?<!\\)(\\\\)*?")')
    def STRING(self, t):
        t.value = t.value[1:-1]
        return t

    @_(r'"""(\n|.)*?"""')
    def MULTILINE_STRING(self, t):
        t.value = t.value[3:-3]
        return t

    @_(r"\'.*?(?<!\\)(\\\\)*\'")
    def CHAR(self, t):
        t.value = t.value[1:-1]
        return t

    @_(r"\n+")
    def newline(self, t):
        self.lineno += t.value.count("\n")

    def error(self, t):
        HascalError("Illegal character '%s':%s" % (t.value, t.lineno))
        exit(1)
