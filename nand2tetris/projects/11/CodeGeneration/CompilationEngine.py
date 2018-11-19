from JackTokenizer import *
from SymbolTable import *
from VMWriter import *


class CompilationEngine:
    """ """
    binaryOp = {'+', '-', '*', '/', '|', '=', '&lt;', '&gt;', '&amp;'}
    unaryOp = {'-', '~'}
    keywordConstant = {'true', 'false', 'null', 'this'}

    # Finished
    def __init__(self, file):
        """ """
        self.label_num = 0
        self.tokenizer = JackTokenizer(file)
        self.advance()

        self.symbols = SymbolTable()
        self.vm = VMWriter()

        self.open_outfile(file)
        self.compile_class()
        self.close_outfile()

    # Finished
    def open_outfile(self, file):
        self.vm.open_outfile(file)

    # Finished
    def close_outfile(self):
        self.vm.close_outfile()

    # Finished
    def advance(self):
        return self.tokenizer.advance()

    # Finished
    def compile_class(self):
        """Compiles a complete class."""
        self.advance()  # skip 'class' keyword
        self.cur_class = self.tokenizer.get_token()  # get class name
        self.advance()  # skip class name
        self.advance()  # skip '{'

        while self.is_class_var_dec():
            self.compile_class_var_dec()

        while self.is_subroutine():
            self.compile_subroutine()

        self.advance()  # skip '}'

    # Finished
    def is_subroutine(self):
        token_type, token = self.tokenizer.peek()
        return token_type == KEYWORD and (token == 'constructor' or token == 'function' or token == 'method')

    # Finished
    def is_class_var_dec(self):
        return self.is_token(KEYWORD, 'static') or self.is_token(KEYWORD, 'field')

    # Finished
    def is_token(self, token_type, token):
        _token_type, _token = self.tokenizer.peek()
        return (token_type, token) == (_token_type, _token)

    # Finished
    def compile_class_var_dec(self):
        """Compiles a static declaration or a field declaration."""
        kind = KIND_MAP[self.tokenizer.get_token()] # get static | filed
        self.advance()
        type = self.tokenizer.get_token()  # get var type
        self.advance()
        name = self.tokenizer.get_token()  # get var name
        self.advance()
        self.symbols.define(name, type, kind)
        while self.is_token(SYMBOL, ','):
            self.advance()
            name = self.tokenizer.get_token()  # get var name
            self.symbols.define(name, type, kind)
        self.advance()  # skip ';'

    # Finished
    def compile_subroutine(self):
        """Compiles a complete method, function, or constructor."""
        token_type, token = self.tokenizer.get_token_type(), self.tokenizer.get_token()  # get subroutine type
        self.advance()  # at return type
        self.advance()  # at subroutine name
        self.cur_subroutine = self.tokenizer.get_token()  # read subroutine name | 'new'
        self.symbols.start_subroutine()
        if token == 'method':
            self.symbols.define('this', self.cur_class, ARG)
        self.advance()
        self.advance() # skip '('
        self.compile_parameter_list()
        self.advance()  # skip ')'
        self.compile_subroutine_body(token)

    # Finished
    def compile_subroutine_body(self, token):
        """ """
        self.advance()  # skip '{'
        while self.is_token(KEYWORD, 'var'):
            self.compile_var_dec()
        self.compile_statements()
        self.advance()  # read '}'

    # Finished
    def compile_parameter_list(self):
        """Compiles a (possibly empty) parameter list, not including the enclosing ()"""

        while not self.is_token(SYMBOL, ')'):

            type = self.tokenizer.get_token()  # get parameter type
            self.advance()
            name = self.tokenizer.get_token()  # get parameter name
            self.advance()
            self.symbols.define(name, type, ARG)
            if self.is_token(SYMBOL, ','):
                self.advance()  # read ','

    # Finished
    def compile_var_dec(self):
        """Compiles a var declaration."""
        kind = KIND_MAP[self.tokenizer.get_token()]  # get 'var' keyword
        self.advance()
        type = self.tokenizer.get_token()  # get var type
        self.advance()
        name = self.tokenizer.get_token()  # get var name
        self.advance()
        self.symbols.define(name, type, kind)
        while self.is_token(SYMBOL, ','):
            self.advance()  # skip ','
            name = self.tokenizer.get_token()  # read var name
            self.symbols.define(name, type, kind)
        self.advance()  # skip ';'

    # Finished
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

    # Finished
    def compile_do(self):
        """Compiles a do statement."""
        self.advance()  # skip 'do' keyword
        self.compile_subroutine_call()
        self.vm.write_pop('temp', 0)
        self.advance()  # skip ';'

    # not Finished
    def compile_subroutine_call(self):
        num_args = 0
        first_name = self.advance()[1]

        if self.is_token(SYMBOL, '.'):
            self.advance()
            last_name = self.advance()[1]
            if first_name in self.symbols.subroutine_symbol or first_name in self.symbols.global_symbol:
                self.write_push(first_name)
                name = self.symbols.type_of(first_name) + '.' + last_name
                num_args += 1
            else:
                name = first_name + '.' + last_name
        else:
            self.vm.write_push('pointer', 0)
            num_args += 1
            name = self.cur_class + '.' + first_name
        self.advance()
        num_args += self.compile_expression_list()
        self.vm.write_call(name, num_args)
        self.advance()

    def compile_let(self):
        """Compiles a let statement."""
        self.advance()  # write 'let'
        self.advance()  # write var name
        if self.is_token(SYMBOL, '['):
            self.advance()  # write '['
            self.compile_expression()
            self.advance()  # write ']'
        self.advance()  # write '='
        self.compile_expression()
        self.advance()  # write ';'

    # not Finished
    def compile_while(self):
        """Compiles a while statement."""
        L1 = self.new_label()
        L2 = self.new_label()

        self.vm.write_label(L1)
        self.advance()  # read 'while'
        self.advance()  # read '('
        self.compile_expression()
        self.advance()  # read ')'
        self.vm.write_vm_cmd('not')  # ~(cond)
        self.vm.write_if(L2)
        self.advance()  # read '{'
        self.compile_statements()
        self.advance()  # read '}'
        self.vm.write_goto(L1)  # goto L1
        self.vm.write_label(L2)

    # not Finished
    def compile_if(self):
        """Compiles an if statement, possibly with a trailing else clause."""
        L1 = self.new_label()
        L2 = self.new_label()

        self.advance()  # read 'if'
        self.advance()  # read '('
        self.compile_expression()
        self.advance()  # read ')'
        self.vm.write_vm_cmd('not')  # ~(cond)
        self.vm.write_if(L1)
        self.advance()  # read '{'
        self.compile_statements()
        self.advance()  # read '}'
        self.vm.write_goto(L2)  # goto L2
        self.vm.write_label(L1)

        if self.is_token(KEYWORD, 'else'):
            self.advance()  # read 'else'
            self.advance()  # read '{'
            self.compile_statements()
            self.advance()  # read '}'
        self.vm.write_label(L2)

    # Finished
    def compile_return(self):
        """Compiles a return statement."""
        self.advance()  # skip 'return'

        if not self.is_token(SYMBOLS, ';'):
            self.compile_expression()
        else:
            self.vm.write_push('constant', 0)
        self.advance()  # skip ';'
        self.vm.write_return()


    def compile_expression(self):
        """Compiles an expression."""

        self.compile_term()
        while self.is_binary_op():
            self.advance()  # write binaryOp
            self.compile_term()

    def compile_term(self):
        """Compiles a term."""
        if self.is_const():
            self.compile_const()

        elif self.is_binary_op():
            self.advance()  # write class | var name
            if self.is_token(SYMBOL, '['):
                self.advance()  # write '['
                self.compile_expression()
                self.advance()  # write ']'
            elif self.is_token(SYMBOL, '('):
                self.advance()  # write '('
                self.compile_expression_list()
                self.advance()  # write ')
            elif self.is_token(SYMBOL, '.'):
                self.advance()  # write '.'
                self.advance()  # write subroutine name
                self.advance()  # write '('
                self.compile_expression_list()
                self.advance()  # write ')'
        elif self.is_unary_op():
            self.advance()  # write unaryOp
            self.compile_term()
        elif self.is_token(SYMBOL, '('):
            self.advance()  # write '('
            self.compile_expression()
            self.advance()  # write ')'

    def compile_const(self):
        token_type, token = self.tokenizer.peek()
        if token_type == INT_CONST:
            self.vm.write_push('constant', token)
        elif token_type == STRING_CONST:
            self.write_string_const(token)

    def write_string_const(self, token):
        """ """

    def compile_expression_list(self):
        """Compiles a (possibly empty) comma-separated list of expressions."""
        if self.is_term():
            self.compile_expression()
        while self.is_token(SYMBOL, ','):
            self.advance()  # write ','
            self.compile_expression()

    def is_const(self):
        token_type, token = self.tokenizer.peek()
        return token_type in [INT_CONST, STRING_CONST] or token in CompilationEngine.keywordConstant

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

    def new_label(self):
        self.label_num += 1
        return 'label' + str(self.label_num)

    def write_push(self, name):
        (type, kind, index) = self.symbols.look_up(name)
        self.vm.write_push(segments[kind], index)

    def write_pop(self, name):
        (type, kind, index) = self.symbols.look_up(name)
        self.vm.write_pop(segments[kind], index)

    def load_pointer(self, func_type):
        if func_type[1] == 'method':
            self.vm.write_push('argument', 0)
            self.vm.write_pop('pointer', 0)
        elif func_type[1] == 'constructor':
            global_vars = self.symbols.index[FIELD]
            self.vm.write_push('constant', global_vars)
            self.vm.write_call('Memory.alloc', 1)
            self.vm.write_pop('pointer', 0)

for k in 'abca':
    print(ord(k))


"""
file_name = '/Users/wen/github/Nand2tetris/nand2tetris/projects/11/test.jack'
s = CompilationEngine(file_name)
print(s.symbols.global_symbol)
"""