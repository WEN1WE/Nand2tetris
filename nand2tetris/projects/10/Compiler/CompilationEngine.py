import JackTokenizer
from JackConstant import *

class CompilationEngine:
    """ """

    def __init__(self, file):
        """ """

        self.tokenizer = JackTokenizer.JackTokenizer(file)
        self.parsed_rules = []
        self.open_outfile(file)
        self.tokenizer.advance()
        self.compile_class()
        self.close_outfile()

    def open_outfile(self, file):
        self.out_file = open(file.replace('.jack', 'MY.xml'), 'w')
        self.tokenizer.open_outfile(file)

    def close_outfile(self):
        self.tokenizer.close_outfile()
        self.out_file.close()

    def write_non_terminal_start(self, rule):
        self.out_file.write('<' + rule + '>\n')
        self.parsed_rules.append(rule)

    def write_non_terminal_end(self):
        rule = self.parsed_rules.pop()
        self.out_file.write('</' + rule + '>\n')

    def write_terminal(self):
        token_type, token = self.tokenizer.token_type, self.tokenizer.token
        self.out_file.write("<" + tokens[token_type] + "> " + self.tokenizer.token + " </" + tokens[token_type] + ">\n")
        self.tokenizer.advance()

    def compile_class(self):
        """Compiles a complete class."""
        self.write_non_terminal_start('class')

        self.write_terminal()           # write 'class'
        self.write_terminal()           # write class name
        self.write_terminal()           # write '{'

        while self.is_class_var_dec():
            self.compile_class_var_dec()

        while self.is_subroutine():
            self.compile_subroutine()

        self.write_terminal()           # write '}'

        self.write_non_terminal_end()

    def is_subroutine(self):
        token_type, token = self.tokenizer.token_type, self.tokenizer.token
        return token_type == KEYWORD and (token == 'constructor' or token == 'function' or token == 'method')

    def is_class_var_dec(self):
        return self.is_token(KEYWORD, 'static') or self.is_token(KEYWORD, 'field')

    def is_token(self, token_type, token):
        return (token_type, token) == (self.tokenizer.token_type, self.tokenizer.token)

    def compile_class_var_dec(self):
        """Compiles a static declaration or a field declaration."""
        self.write_non_terminal_start('classVarDec')
        self.write_terminal()           # write static | filed
        self.write_terminal()           # write token_type
        self.write_terminal()           # write token
        while self.is_token(SYMBOL, ','):
            self.write_terminal()       # write ','
            self.write_terminal()       # write token
        self.write_terminal()           # write ';'

        self.write_non_terminal_end()

    def compile_subroutine(self):
        """Compiles a complete method, function, or constructor."""
        self.write_non_terminal_start('subroutineDec')
        self.write_terminal()           # write subroutine type
        self.write_terminal()           # write subroutine return type | constructor name
        self.write_terminal()           # write subroutine name | 'new'
        self.write_terminal()           # write '('
        self.compile_parameter_list()
        self.write_terminal()           # write ')'
        self.compile_subroutine_body()
        self.write_non_terminal_end()

    def compile_subroutine_body(self):
        """ """
        self.write_non_terminal_start('subroutineBody')
        self.write_terminal()           # write '{'
        while self.is_token(KEYWORD, 'var'):
            self.compile_var_dec()
        self.compile_statements()
        self.write_terminal()
        self.write_non_terminal_end()

    def compile_parameter_list(self):
        """Compiles a (possibly empty) parameter list, not including the enclosing ()"""
        self.write_non_terminal_start('parameterList')
        while not self.is_token(SYMBOL, ')'):
            self.write_terminal()       # write parameter type
            self.write_terminal()       # write parameter name
            if self.is_token(SYMBOL, ','):
                self.write_terminal()   # write ','
        self.write_non_terminal_end()

    def compile_var_dec(self):
        """Compiles a var declaration."""
        self.write_non_terminal_start('varDec')
        self.write_terminal()           # write 'var'
        self.write_terminal()           # write var type
        self.write_terminal()           # write var name
        while self.is_token(SYMBOL, ','):
            self.write_terminal()       # write ','
            self.write_terminal()       # write var name
        self.write_terminal()           # write ';'
        self.write_non_terminal_end()


    def compile_statements(self):
        """Compiles a sequence of statements, not including the enclosing {}."""
        self.write_non_terminal_start('statements')
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
        self.write_non_terminal_end()

    def compile_do(self):
        """Compiles a do statement."""

    def compile_let(self):
        """Compiles a let statement."""

    def compile_while(self):
        """Compiles a while statement."""

    def compile_return(self):
        """Compiles a return statement."""

    def compile_if(self):
        """Compiles an if statement, possibly with a trailing else clause."""

    def compile_expression(self):
        """Compiles an expression."""

    def compile_term(self):
        """Compiles a term."""

    def compile_expression_list(self):
        """Compiles a (possibly empty) comma-separated list of expressions."""

file_name = '/Users/wen/github/Nand2tetris/nand2tetris/projects/10/Main.jack'
s = CompilationEngine(file_name)
print(s.tokenizer.tokens)

