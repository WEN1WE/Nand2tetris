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
        name = self.tokenizer.get_token()
        self.compile_subroutine_call(name)
        self.vm.write_pop('temp', 0)
        self.advance()  # skip ';'

    # Finished
    def compile_subroutine_call(self, name):
        num_args = 0

        if self.is_token(SYMBOL, '.'):
            self.advance() # skip '.'
            method_name = self.tokenizer.get_token()
            self.advance()  # skip last_name
            if name in self.symbols.subroutine_symbol or name in self.symbols.global_symbol:
                self.write_push(name)
                full_name = self.symbols.type_of(name) + '.' + method_name
                num_args += 1
            else:
                full_name = name + '.' + method_name
        else:
            self.vm.write_push('pointer', 0)
            num_args += 1
            full_name = self.cur_class + '.' + name
        self.advance()  # skip '('
        num_args += self.compile_expression_list()
        self.vm.write_call(full_name, num_args)
        self.advance()  # skip ')'


    """
    def compile_subroutine_call(self, name):
        (type, kind, index) = self.symbols.look_up(name)
    """

    # Finished
    def compile_let(self):
        """Compiles a let statement."""
        self.advance()  # skip 'let'
        name = self.tokenizer.get_token()
        self.advance()  # skip name
        subscript = self.is_token(SYMBOLS, '[')
        if subscript:
            self.compile_base_plus_index(name)
        self.advance()  # skip '='
        self.compile_expression()  # calculate expression
        self.advance()  # write ';'
        if subscript:
            self.pop_array_element()  # *(base+index) == expr
        else:
            self.write_pop(name)

    # Finished
    def pop_array_element(self):
        self.vm.write_pop('temp', 1)  # pop expr value to temp register
        self.vm.write_pop('pointer', 1)  # pop base+index into 'that' register
        self.vm.write_push('temp', 1)  # push expr back into stack
        self.vm.write_pop('that', 0)  # pop value into *(base+index)

    # Finished
    def compile_base_plus_index(self, name):
        self.write_push(name)
        self.advance()  # skip '['
        self.compile_expression()  # push index into stack
        self.advance()  # skip '['
        self.vm.write_vm_cmd('add')  # base+index

    # Finished
    def compile_while(self):
        """Compiles a while statement."""
        L1 = self.new_label()
        L2 = self.new_label()

        self.vm.write_label(L1)
        self.advance()  # skip 'while'
        self.advance()  # skip '('
        self.compile_expression()
        self.advance()  # skip ')'
        self.vm.write_vm_cmd('not')  # ~(cond)
        self.vm.write_if(L2)
        self.advance()  # skip '{'
        self.compile_statements()
        self.advance()  # rskip '}'
        self.vm.write_goto(L1)  # goto L1
        self.vm.write_label(L2)

    # Finished
    def compile_if(self):
        """Compiles an if statement, possibly with a trailing else clause."""
        L1 = self.new_label()
        L2 = self.new_label()

        self.advance()  # skip 'if'
        self.advance()  # skip '('
        self.compile_expression()
        self.advance()  # skip ')'
        self.vm.write_vm_cmd('not')  # ~(cond)
        self.vm.write_if(L1)
        self.advance()  # skip '{'
        self.compile_statements()
        self.advance()  # skip '}'
        self.vm.write_goto(L2)  # goto L2
        self.vm.write_label(L1)

        if self.is_token(KEYWORD, 'else'):
            self.advance()  # skip 'else'
            self.advance()  # skip '{'
            self.compile_statements()
            self.advance()  # skip '}'
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

    # Finished
    def compile_expression(self):
        """Compiles an expression."""
        self.compile_term()
        while self.is_binary_op():
            binary_op = self.tokenizer.get_token()
            self.advance()  # skip op
            self.compile_term()
            self.vm.write_vm_cmd(VM_BINORY_CMDS[binary_op])

    # Finished
    def compile_term(self):
        """Compiles a term."""
        token_type, token = self.tokenizer.peek()
        if self.is_const():
            self.compile_const()
        elif self.is_unary_op():
            self.advance()  # write unaryOp
            self.compile_term()
        elif self.is_token(SYMBOL, '('):
            self.advance()  # write '('
            self.compile_expression()
            self.advance()  # write ')'
        elif token_type is IDENTIFIER:
            self.advance()  # skip class name
            if self.is_token(SYMBOLS, '['):
                self.compile_array_subscript(token)
            elif self.is_token(SYMBOLS, '.'):
                self.compile_subroutine_call(token)
            else:
                self.write_push(token)

    # Finished
    def compile_array_subscript(self, name):
        self.write_push(name)
        self.advance()  # skip name
        self.advance()  # skip '['
        self.compile_expression()  # push index into stack
        self.advance()  # skip ']'
        self.vm.write_vm_cmd('add')
        self.vm.write_pop('pointer', 1)  # pop into 'that' ptr
        self.vm.write_push('that', 0)  # push *(base+index) into stack

    # Finished
    def compile_const(self):
        token_type, token = self.tokenizer.peek()
        if token_type == INT_CONST:
            self.vm.write_push('constant', token)
        elif token_type == STRING_CONST:
            self.write_string_const(token)
        elif token_type == CompilationEngine.keywordConstant:
            self.compile_kew_const(token)

    # Finished
    def compile_kew_const(self, kwd):
        if kwd == 'this':
            self.vm.write_push('pointer', 0)
        elif kwd == 'true':
            self.vm.write_push('constant', 1)
            self.vm.write_vm_cmd('neg')
        else:
            self.vm.write_push('constant', 0)

    # Finished
    def write_string_const(self, token):
        """ """
        self.vm.write_push('constant', len(token))
        self.vm.write_call('String.new', 1)  # String.new(len(str))
        for c in token:
            self.vm.write_push('constant', ord(c))
            self.vm.write_call('String.appendChar', 2)  # String.appendChar(c)

    # Finished
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
        self.vm.write_push(SEGMENTS[kind], index)

    def write_pop(self, name):
        (type, kind, index) = self.symbols.look_up(name)
        self.vm.write_pop(SEGMENTS[kind], index)

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