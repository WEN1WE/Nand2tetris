# Token types
KEYWORD = 0
SYMBOL = 1
IDENTIFIER = 2
INT_CONST = 3
STRING_CONST = 4

KEYWORDS = {"class", "constructor", "function", "method", "field", "static", "var", "int", "char", "boolean",
            "void", "true", "false", "null", "this", "let", "do", "if", "else", "while", "return"}

SYMBOLS = {'{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&', '<', '>', '=', '~'}


# kind of scope
STATIC = 0
FIELD = 1
ARG = 2
VAR = 3

KIND_MAP = {'static': STATIC, 'field': FIELD, 'var': VAR}

segments = {VAR: 'local', STATIC: 'static', FIELD: 'this', ARG: 'argument'}