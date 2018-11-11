import JackTokenizer
from JackConstant import *

class CompilationEngine:
    """ """

    def __init__(self, file):
        """ """

        self.tokenizer = JackTokenizer.JackTokenizer(file)
        self.parsed_rules = []
#        self.open_outfile(file)
#        self.compile_class()
#        self.close_out()

    def open_outfile(self, file):
        self.out_file = open(file.replace('.jack', 'MY.xml'), 'w')
        self.tokenizer.open_outfile(file)

    def close_out(self):
        self.tokenizer.close_outfile()
        self.out_file.close()

    def write_non_terminal_start(self, rule):
        self.out_file.write('<' + rule + '>\n')
        self.parsed_rules.append(rule)

    def write_non_terminal_end(self):
        rule = self.parsed_rules.pop()
        self.out_file.write('</' + rule + '>\n')

    def write_terminal(self):
        self.tokenizer.advance()
        self.out_file.write("<" + self.tokenizer.token_type + "> " + self.tokenizer.token + " </" + self.tokenizer.token_type + ">\n")

    def compile_class(self):
        """Compiles a complete class."""
        self.write_non_terminal_start('class')

        self.write_terminal()      # write 'class'
        self.write_terminal()      # write class name
        self.write_terminal()      # write '{'

        while self.is_class_var_dec():
            self.compile_class_var_dec()

        while self.is_subroutine():
            self.compile_subroutine()

        self.write_non_terminal_end()

    def is_subroutine(self):
        token_type, token = self.tokenizer.token_type, self.tokenizer.token
        return token_type == KEYWORD and (token == 'constructor' or token == 'function' or token == 'method')

    def is_class_var_dec(self):
        return self.is_token(KEYWORD, 'static') or self.is_token(KEYWORD, 'field')

    def is_token(self, token_type, token):
        self.tokenizer.advance()
        return (token_type, token) == (self.tokenizer.token_type, self.tokenizer.token)

    def compile_class_var_dec(self):
        """Compiles a static declaration or a field declaration."""

    def compile_subroutine(self):
        """Compiles a complete method, function, or constructor."""

    def compile_parameter_list(self):
        """Compiles a (possibly empty) parameter list, not including the enclosing ()"""

    def compile_var_dec(self):
        """Compiles a var declaration."""

    def compile_statements(self):
        """Compiles a sequence of statements, not including the enclosing {}."""

    def compile_do(self):
        """Compiles a do statement."""

    def complie_let(self):
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

