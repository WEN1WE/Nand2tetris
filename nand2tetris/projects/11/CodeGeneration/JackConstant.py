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

SEGMENTS = {VAR: 'local', STATIC: 'static', FIELD: 'this', ARG: 'argument'}

# VM Writer Support
VM_BINORY_CMDS = {'+': 'add', '-': 'sub', '*': 'call Math.multiply 2', '/': 'call Math.divide 2',
           '<': 'lt', '>': 'gt', '=': 'eq', '&': 'and', '|': 'or'}
VM_UNARY_CMDS = {'-': 'neg', '~': 'not'}