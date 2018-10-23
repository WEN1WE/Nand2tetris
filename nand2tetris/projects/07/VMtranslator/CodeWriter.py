class CodeWriter:
    """Translate VM commands into Hack assembly code."""

    def __init__(self, out_file_name):
        """Opens the output file."""

    def set_file_name(self):
        """Informs the code writer that the translation of a new VM file is started."""

    @staticmethod
    def write_arithmetic(command):
        """Writes the assembly code that is the translation of the given arithmetic command."""
        if command == 'neg':
            return unary_operator('-')
        elif command == 'not':
            return unary_operator('!')
        elif command == 'add':
            return binary_operator('+')
        elif command == 'sub':
            return binary_operator('-')
        elif command == 'and':
            return binary_operator('&')
        elif command == 'or':
            return binary_operator('|')
        elif command == 'eq':
            return compare('JEQ')
        elif command == 'lt':
            return compare('JLT')
        elif command == 'gt':
            return compare('JGT')

    @staticmethod
    def write_push_pop(command, segment, index):
        """Write the assembly code that is the translation of the push or pop command."""
        if command == 'C_PUSH':
            return push(segment, index)



    def close(self):
        """Closes the output file."""

    def wirte_init(self):
        """Write the assembly code that the VM initialization."""

    def write_label(self):
        """Write the assembly code that is the translation of the label command."""

    def wirte_goto(self):
        """Write the assembly code that is the translation of the goto command."""

    def write_if(self):
        """Write the assembly code that is the translation of the if command."""

    def write_call(self):
        """Write the assembly code that is the translation of the call command."""

    def write_return(self):
        """Write the assembly code that is the translation of the return command."""

    def write_function(self):
        """Write the assembly code that is the translation of the function command."""

# Generator A or C or L commands.
def a_command(value):
    """Returns @value."""
    return '@' + value + '\n'


def c_command(dest, comp, jump):
    """Returns dest=comp;jump."""
    if dest:
        return dest + '=' + comp + '\n'
    elif jump:
        return comp + ';' + jump + '\n'
    else:
        return comp + '\n'


def c_destination(dest, comp):
    """Returns dest=comp."""
    return c_command(dest, comp, None)


def c_jump(comp, jump):
    """Returns comp;jump."""
    return c_command(None, comp, jump)


def l_command(label):
    """Returns (label)."""
    return '(' + label + ')\n'

# Methods to operate SP
def inc_sp():
    """ SP += 1 """
    return a_command('SP') + c_destination('M', 'M+1')


def dec_sp():
    """ SP -= 1 """
    return a_command('SP') + c_destination('M', 'M-1')


def load_sp():
    """ A = SP """
    return a_command('SP') + c_destination('A', 'M')

# Methods to operate stack
def stack_to_dest(dest):
    """ dest = *SP """
    return load_sp() + c_destination(dest, 'M')


def comp_to_stack(comp):
    """ *SP = comp """
    return load_sp() + c_destination('M', comp)


def val_to_stack(val):
    """ A = val
        D = A
        *SP = D
    """
    return (a_command(val)
            + c_destination('D', 'A')
            + comp_to_stack('D'))


def load_segment(segment, index):
    a_command(index)                # A = index
    c_destination('D', 'A')         # D = A
    a_command(segment)
    c_destination('A', 'M')         # A = segment
    c_destination('A', 'D+A')       # A = D + A


def mem_to_stack(segment, index):
    load_segment(segment, index)
    c_destination('D', 'M')
    comp_to_stack('D')

# Methods to operate register
def reg_to_stack(seg, index):
    reg_to_dest('D', seg)
    comp_to_stack('D')


def reg_to_dest(dest, reg):
    a_command(reg)
    c_destination(dest, 'M')



# Arithmetic and logic operations.
def unary_operator(operator):
    """ SP -= 1
        *SP = operator + *SP
        SP += 1 """
    return (dec_sp()
            + comp_to_stack(operator + 'M')
            + inc_sp())


def binary_operator(operator):
    """ SP -= 1
        D = *SP
        SP -= 1
        M = M operator D
        SP += 1 """
    return (dec_sp()
            + stack_to_dest('D')
            + dec_sp()
            + comp_to_stack('M' + operator + 'D')
            + inc_sp())


def compare(operator):
    """ SP -= 1
        D = *SP
        SP -= 1
        A = *SP
        D = A - D

        @jump
        D;operator

        @end
        *SP = 0

        (jump)
        *SP = -1

        (end)
        SP += 1 """
    return (dec_sp()
            + stack_to_dest('D')
            + dec_sp()
            + stack_to_dest('A')
            + c_destination('D', 'A-D')
            + a_command('jump')
            + c_jump('D', operator)
            + a_command('end')
            + comp_to_stack('0')
            + l_command('jump')
            + comp_to_stack('-1')
            + l_command('end')
            + inc_sp())


def is_constant_segment(segment):
    return segment == 'constant'


def is_memory_segment(segment):
    return segment in ['argument', 'local', 'this', 'that']


def is_reg_segment(segment):
    return segment in ['pointer', 'temp']


def is_static_segement(segment):
    return segment == 'static'


def push(segment, index):
    if is_constant_segment(segment):
        return val_to_stack(index)
    elif is_memory_segment(segment):
        return mem_to_stack(segment, index)
    elif is_reg_segment(segment):
        reg_to_stack(segment, index)










print(CodeWriter.write_arithmetic('and'))