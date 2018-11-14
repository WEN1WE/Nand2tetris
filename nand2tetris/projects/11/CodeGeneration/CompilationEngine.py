from JackTokenizer import *
from SymbolTable import *
from VMWriter import *

class CompilationEngine:
    """ """
    binaryOp = {'+', '-', '*', '/', '|', '=', '&lt;', '&gt;', '&amp;'}
    unaryOp = {'-', '~'}
    keywordConstant = {'true', 'false', 'null', 'this'}

    def __init__(self, file):
        """ """
        self.tokenizer = JackTokenizer(file)
        self.symbols = SymbolTable()
        self.writer = VMWriter()

        self.open_outfile(file)
        self.compile_class()
        self.close_outfile()

    def open_outfile(self, file):
        self.writer.open_outfile(file)

    def close_outfile(self):
        self.writer.close_outfile()

    def advance(self):
        return self.tokenizer.advance()

    def compile_class(self):
        """Compiles a complete class."""
        self.advance()  # read 'class' keyword
        self.cur_class = self.advance()[1]  # read class name
        self.advance()  # read '{'

        while self.is_class_var_dec():
            self.compile_class_var_dec()

        while self.is_subroutine():
            self.compile_subroutine()

        self.advance()  # read '}'

    def is_subroutine(self):
        token_type, token = self.tokenizer.peek()
        return token_type == KEYWORD and (token == 'constructor' or token == 'function' or token == 'method')

    def is_class_var_dec(self):
        return self.is_token(KEYWORD, 'static') or self.is_token(KEYWORD, 'field')

    def is_token(self, token_type, token):
        _token_type, _token = self.tokenizer.peek()
        return (token_type, token) == (_token_type, _token)

    def compile_class_var_dec(self):
        """Compiles a static declaration or a field declaration."""
        kind = self.advance()[1]  # read static | filed
        type = self.advance()[1]  # read var type
        name = self.advance()[1]  # read var name
        self.symbols.define(name, type, kind)
        while self.is_token(SYMBOL, ','):
            self.advance()  # read ','
            name = self.advance()[1]
            self.symbols.define(name, type, kind)
        self.advance()  # get ';'

    def compile_subroutine(self):
        """Compiles a complete method, function, or constructor."""
        token_type, token = self.advance()  # read subroutine type
        self.advance()  # read subroutine return type | constructor name
        self.cur_subroutine = self.advance()[1]  # read subroutine name | 'new'
        self.symbols.start_subroutine()
        if token == 'method':
            self.symbols.define('this', self.cur_class, ARG)
        self.advance()  # read '('
        self.compile_parameter_list()
        self.advance()  # read ')'
        self.compile_subroutine_body(token)

    def compile_subroutine_body(self, token):
        """ """
        self.advance()  # read '{'
        while self.is_token(KEYWORD, 'var'):
            self.compile_var_dec()
        self.compile_statements()
        self.advance()  # read '}'

    def compile_parameter_list(self):
        """Compiles a (possibly empty) parameter list, not including the enclosing ()"""

        while not self.is_token(SYMBOL, ')'):
            type = self.advance()[1]  # read parameter type
            name = self.advance()[1]  # read parameter name
            self.symbols.define(name, type, ARG)
            if self.is_token(SYMBOL, ','):
                self.advance()  # read ','

    def compile_var_dec(self):
        """Compiles a var declaration."""
        kind = self.advance()[1]  # read 'var'
        type = self.advance()[1]  # read var type
        name = self.advance()[1]  # read var name
        self.symbols.define(name, type, kind)
        while self.is_token(SYMBOL, ','):
            self.advance()  # read ','
            name = self.advance()[1]  # read var name
            self.symbols.define(name, type, kind)
        self.advance()  # read ';'

    def compile_statements(self):
        """Compiles a sequence of statements, not including the enclosing {}."""
        while True:
            if self.is_token(KEYWORD, 'do'):
                self.compile_do()
            elif self.is_token(KEYWORD, 'let'):
                self.compile_let()
            elif self.is_token(KEYWORD, 'if'):
                self.compile_if()
            elif self.is_token(KEYWORD, 'while'):
                self.compile_while()
            elif self.is_token(KEYWORD, 'return'):
                self.compile_return()
            else:
                break

    def compile_do(self):
        """Compiles a do statement."""
        self.advance()  # read 'do' keyword
        self.compile_subroutine_call()
        self.writer.write_pop('temp', 0)
        self.advance()  # write ';'

    def compile_subroutine_call(self):
        if self.is_token(SYMBOL, '.'):
            self.write_terminal()  # write '.'
            self.write_terminal()  # write subroutine name
        self.write_terminal()  # write '('
        self.compile_expression_list()  #


    def compile_let(self):
        """Compiles a let statement."""
        self.write_non_terminal_start('letStatement')
        self.write_terminal()  # write 'let'
        self.write_terminal()  # write var name
        if self.is_token(SYMBOL, '['):
            self.write_terminal()  # write '['
            self.compile_expression()
            self.write_terminal()  # write ']'
        self.write_terminal()  # write '='
        self.compile_expression()
        self.write_terminal()  # write ';'
        self.write_non_terminal_end()

    def compile_while(self):
        """Compiles a while statement."""
        self.write_non_terminal_start('whileStatement')
        self.write_terminal()  # write 'while'
        self.write_terminal()  # write '('
        self.compile_expression()
        self.write_terminal()  # write ')'
        self.write_terminal()  # write '{'
        self.compile_statements()
        self.write_terminal()  # write '}'
        self.write_non_terminal_end()

    def compile_return(self):
        """Compiles a return statement."""
        self.write_non_terminal_start('returnStatement')
        self.write_terminal()  # write 'return'
        while self.is_term():
            self.compile_expression()
        self.write_terminal()  # write ';'
        self.write_non_terminal_end()

    def compile_if(self):
        """Compiles an if statement, possibly with a trailing else clause."""
        self.write_non_terminal_start('ifStatement')
        self.write_terminal()  # write 'if'
        self.write_terminal()  # write '('
        self.compile_expression()
        self.write_terminal()  # write ')'
        self.write_terminal()  # write '{'
        self.compile_statements()
        self.write_terminal()  # write '}'
        if self.is_token(KEYWORD, 'else'):
            self.write_terminal()  # write 'else'
            self.write_terminal()  # write '{'
            self.compile_statements()
            self.write_terminal()
        self.write_non_terminal_end()

    def compile_expression(self):
        """Compiles an expression."""
        self.write_non_terminal_start('expression')
        self.compile_term()
        while self.is_binary_op():
            self.write_terminal()  # write binaryOp
            self.compile_term()
        self.write_non_terminal_end()

    def compile_term(self):
        """Compiles a term."""

        token_type, token = self.tokenizer.peek()
        if token_type in [INT_CONST, STRING_CONST] or token in CompilationEngine.keywordConstant:
            self.write_terminal()  # write constant
        elif token_type is IDENTIFIER:
            self.write_terminal()  # write class | var name
            if self.is_token(SYMBOL, '['):
                self.write_terminal()  # write '['
                self.compile_expression()
                self.write_terminal()  # write ']'
            elif self.is_token(SYMBOL, '('):
                self.write_terminal()  # write '('
                self.compile_expression_list()
                self.write_terminal()  # write ')
            elif self.is_token(SYMBOL, '.'):
                self.write_terminal()  # write '.'
                self.write_terminal()  # write subroutine name
                self.write_terminal()  # write '('
                self.compile_expression_list()
                self.write_terminal()  # write ')'
        elif token in CompilationEngine.unaryOp:
            self.write_terminal()  # write unaryOp
            self.compile_term()
        elif self.is_token(SYMBOL, '('):
            self.write_terminal()  # write '('
            self.compile_expression()
            self.write_terminal()  # write ')'


    def compile_expression_list(self):
        """Compiles a (possibly empty) comma-separated list of expressions."""

        if self.is_term():
            self.compile_expression()
        while self.is_token(SYMBOL, ','):
            self.write_terminal()  # write ','
            self.compile_expression()

    def is_binary_op(self):
        token_type, token = self.tokenizer.peek()
        return token_type == SYMBOL and token in CompilationEngine.binaryOp

    def is_unary_op(self):
        token_type, token = self.tokenizer.peek()
        return token_type == SYMBOL and token in CompilationEngine.unaryOp

    def is_keyword_constant(self):
        token_type, token = self.tokenizer.peek()
        return token_type == KEYWORD and token in CompilationEngine.keywordConstant

    def is_term(self):
        token_type, token = self.tokenizer.peek()
        return token_type in [INT_CONST, STRING_CONST] or self.is_keyword_constant() or token_type is IDENTIFIER or self.is_unary_op() or self.is_token(SYMBOL, '(')


file_name = '/Users/wen/github/Nand2tetris/nand2tetris/projects/10/SquareGame.jack'
s = CompilationEngine(file_name)
print(s.tokenizer.tokens)