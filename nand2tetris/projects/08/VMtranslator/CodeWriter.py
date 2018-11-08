from Parser import *
import os

class CodeWriter:
    """Translate VM commands into Hack assembly code."""

    def __init__(self, out_file_name):
        """Opens the output file."""
        self.out_file = open(out_file_name, 'w')
        self.input_file = ''
        self.count = 0

    def set_file_name(self, file_name):
        """Informs the code writer that the translation of a new VM file is started."""
        print("Start translating file: " + file_name)
        self.input_file, ext = os.path.splitext(file_name)

    def close_file(self):
        """Closes the output file."""
        self.out_file.close()

    def write_init(self):
        """Writes the assembly code that the VM initialization."""
        self.a_command('256')                      # @256
        self.c_destination('D', 'A')               # D=A
        self.a_command('SP')                       # @SP
        self.c_destination('M', 'D')               # SP=D=256
        self.write_call('Sys.init', 0)

    def write_label(self, label):
        """Writes the assembly code that is the translation of the label command."""
        self.l_command(label)

    def write_goto(self, label):
        """Writes the assembly code that is the translation of the goto command."""
        self.a_command(label)
        self.c_jump('0', 'JMP')

    def write_if(self, label):
        """Writes the assembly code that is the translation of the if-goto command."""
        self.pop_to_dest('D')
        self.a_command(label)
        self.c_jump('D', 'JNE')

    def write_call(self, function_name, num_args):
        """Write the assembly code that is the translation of the call command."""
        return_address = self.new_label()
        self.push(S_CONST, return_address)          # push return_address
        self.push(S_REG, R_LCL)                     # push LCL
        self.push(S_REG, R_ARG)                     # push ARG
        self.push(S_REG, R_THIS)                    # push THIS
        self.push(S_REG, R_THAT)                    # push THAT
        self.offset_sp(num_args+5)                  # D = SP - n - 5
        self.comp_to_reg(R_ARG, 'D')                # LCL = D
        self.reg_to_reg(R_LCL, R_SP)                # LCL=SP
        self.a_command(function_name)
        self.c_jump('0', 'JMP')                     # goto f
        self.l_command(return_address)              # (return_address)

    def write_function(self, funciton_name, num_locals):
        """Writes the assembly code that is the trans of the given function command."""
        self.l_command(funciton_name)
        for i in range(num_locals):
            self.push(S_CONST, 0)

    def write_return(self):
        """Writes the assembly code that is the translation of the return command."""
        self.reg_to_reg(R_FRAME, R_LCL)             # FRAME = LCL
        self.a_command('5')
        self.c_destination('A', 'D-A')
        self.c_destination('D', 'M')
        self.comp_to_reg(R_RET, 'D')                # RET = *(FRAME - 5)
        self.pop(S_ARG, 0)                          # *ARG = return value
        self.reg_to_dest('D', R_ARG)
        self.comp_to_reg(R_SP, 'D+1')               # SP = ARG + 1
        self.prev_frame_to_reg(R_THAT)              # THAT = *(FRAME - 1)
        self.prev_frame_to_reg(R_THIS)              # THIS = *(FRAME - 2)
        self.prev_frame_to_reg(R_ARG)               # ARG = *(FRAME - 3)
        self.prev_frame_to_reg(R_LCL)               # LCL = *(FRAME - 4)
        self.reg_to_dest('A', R_RET)                # A = RET
        self.c_jump('0', 'JMP')                     # goto RET

    def prev_frame_to_reg(self, reg):
        """ reg = *(FRAME - 1) """
        self.reg_to_dest('D', R_FRAME)              # D = FRAME
        self.c_destination('D', 'D-1')              # D = FRAME - 1
        self.comp_to_reg(R_FRAME, 'D')              # FRAME = FRAME - 1
        self.c_destination('A', 'D')
        self.c_destination('D', 'M')                # D = *(FRAME - 1)
        self.comp_to_reg(reg, 'D')                  # reg = D

    def write_arithmetic(self, command):
        """Writes the assembly code that is the translation of the given arithmetic command."""
        if command == 'neg':
            self.unary_operator('-')
        elif command == 'not':
            self.unary_operator('!')
        elif command == 'add':
            self.binary_operator('+')
        elif command == 'sub':
            self.binary_operator('-')
        elif command == 'and':
            self.binary_operator('&')
        elif command == 'or':
            self.binary_operator('|')
        elif command == 'eq':
            self.compare('JEQ')
        elif command == 'lt':
            self.compare('JLT')
        elif command == 'gt':
            self.compare('JGT')

    def write_push_pop(self, command, seg, index):
        """Writes the assembly code that is the translation of the given C_PUSH or C_POP command."""
        if command == C_PUSH:
            self.push(seg, index)
        elif command == C_POP:
            self.pop(seg, index)

# ***************** Helper methods for push and pop. *************************************
    def push(self, seg, index):
        if CodeWriter.is_const_seg(seg):
            self.val_to_stack(index)
        elif CodeWriter.is_mem_seg(seg):
            seg = CodeWriter.change_name(seg)
            self.mem_to_stack(seg, index)
        elif CodeWriter.is_reg_seg(seg):
            self.reg_to_stack(seg, index)
        elif CodeWriter.is_static_seg(seg):
            self.static_to_stack(seg, index)

        self.inc_sp()

    def pop(self, seg, index):
        self.dec_sp()                              # SP -= 1
        if CodeWriter.is_mem_seg(seg):
            seg = CodeWriter.change_name(seg)
            self.stack_to_mem(seg, index)
        elif CodeWriter.is_reg_seg(seg):
            self.stack_to_reg(seg, index)
        elif self.is_static_seg(seg):
            self.stack_to_static(seg, index)

    def pop_to_dest(self, dest):
        self.dec_sp()
        self.stack_to_dest(dest)

# ***************** Gets segment type or changes segment name to special label. ***********
    @staticmethod
    def is_mem_seg(seg):
        return seg in [S_LCL, S_ARG, S_THIS, S_THAT]

    @staticmethod
    def is_reg_seg(seg):
        return seg in [S_REG, S_PTR, S_TEMP]

    @staticmethod
    def is_static_seg(seg):
        return seg == S_STATIC

    @staticmethod
    def is_const_seg(seg):
        return seg == S_CONST                      #

    @staticmethod
    def change_name(seg):
        return {S_LCL: 'LCL', S_ARG: 'ARG', S_THIS: 'THIS', S_THAT: 'THAT', 'reg': R_R0, 'pointer': R_PTR, 'temp': R_TEMP}[seg]
# *****************************************************************************************

# ***************** Arithmetic and logic operations. **************************************
    def unary_operator(self, operator):
        self.dec_sp()                              # SP -= 1
        self.stack_to_dest('D')                    # D = *SP
        self.c_destination('D', operator+'D')      # D = operator + D
        self.comp_to_stack('D')                    # *SP = D
        self.inc_sp()                              # SP += 1

    def binary_operator(self, operator):
        self.dec_sp()                              # SP -= 1
        self.stack_to_dest('D')                    # D = *SP
        self.dec_sp()                              # SP -= 1
        self.stack_to_dest('A')                    # A = *SP
        self.c_destination('D', 'A'+operator+'D')  # D = A operator D
        self.comp_to_stack('D')                    # *SP = D
        self.inc_sp()                              # SP += 1

    def compare(self, operator):
        self.dec_sp()                              # SP -= 1
        self.stack_to_dest('D')                    # D = *SP
        self.dec_sp()                              # SP -= 1
        self.stack_to_dest('A')                    # A = *SP
        self.c_destination('D', 'A-D')             # D = A-D
        self.a_command('jump' + str(self.count))   # @jump
        self.c_jump('D', operator)                 # D;operator
        self.comp_to_stack('0')                    # *SP = 0
        self.a_command('end' + str(self.count))    # @end
        self.c_jump('0', 'JMP')                    # 0;JMP
        self.l_command('jump' + str(self.count))   # (jump)
        self.comp_to_stack('-1')                   # *SP = -1
        self.l_command('end' + str(self.count))    # (end)
        self.inc_sp()                              # SP += 1
        self.count += 1
# *****************************************************************************************


# ***************** Methods to store values into the stack. *******************************
    def comp_to_stack(self, comp):
        """ *SP = comp """
        self.load_sp()                             # A = SP
        self.c_destination('M', comp)              # *SP = comp

    def val_to_stack(self, val):
        """ *SP = val """
        self.a_command(str(val))                   # A = val
        self.c_destination('D', 'A')               # D = A
        self.comp_to_stack('D')                    # *SP = D

    def mem_to_stack(self, seg, index):
        self.load_seg(seg, index)                  # A = segment + index
        self.c_destination('D', 'M')               # D = *(segment + index)
        self.comp_to_stack('D')                    # *SP = D

    def reg_to_stack(self, seg, index):
        self.reg_to_dest('D', CodeWriter.change_name(seg) + int(index))
        self.comp_to_stack('D')

    def static_to_stack(self, seg, index):
        self.a_command(self.input_file + '.' + str(index))
        self.c_destination('D', 'M')
        self.comp_to_stack('D')
# *****************************************************************************************


# ***************** Methods to get data from the stack. ***********************************
    def stack_to_dest(self, dest):
        """ dest = *SP """
        self.load_sp()                             # A = SP
        self.c_destination(dest, 'M')              # dest = *SP

    def stack_to_mem(self, seg, index):
        """ *(seg + index) = *SP"""
        self.load_seg(seg, index)                  # D = seg + index
        self.comp_to_reg(R_R15, 'D')               # R_R15 = D
        self.stack_to_dest('D')                    # D = *SP
        self.reg_to_dest('A', R_R15)               # A = R_R15
        self.c_destination('M', 'D')               # *(seg + index) = D

    def stack_to_reg(self, seg, index):
        """ reg = *SP"""
        self.stack_to_dest('D')                    # D = *SP
        seg = CodeWriter.change_name(seg)
        self.comp_to_reg(seg+int(index), 'D')

    def static_name(self, index):
        return self.input_file + '.' + str(index)

    def stack_to_static(self, seg, index):
        self.stack_to_dest('D')
        self.a_command(self.input_file + '.' + str(index))
        self.c_destination('M', 'D')
# *****************************************************************************************


# ***************** Methods about segment *************************************************
    def load_seg(self, seg, index):
        """ A = seg + index"""
        self.a_command(index)                      # A = index
        self.c_destination('D', 'A')               # D = A
        self.a_command(seg)
        self.c_destination('A', 'M')               # A = seg
        self.c_destination('AD', 'D+A')            # AD = D + A
# *****************************************************************************************


# ***************** Methods about register ************************************************
    def reg_to_dest(self, dest, reg):
        """ dest = reg """
        self.a_command('R' + str(reg))             # @R#
        self.c_destination(dest, 'M')              # dest = R#

    def comp_to_reg(self, reg, comp):
        """ reg = comp """
        self.a_command('R' + str(reg))             # @R#
        self.c_destination('M', comp)              # R# = dest

    def reg_to_reg(self, dest, src):
        """ dest = src """
        self.reg_to_dest('D', src)
        self.comp_to_reg(dest, 'D')
# *****************************************************************************************


# **************** Methods about SP *******************************************************
    def inc_sp(self):
        """ SP += 1 """
        self.a_command('SP')                       # @SP
        self.c_destination('M', 'M+1')             # SP += 1

    def dec_sp(self):
        """ SP -= 1 """
        self.a_command('SP')                       # @SP
        self.c_destination('M', 'M-1')             # SP -= 1

    def load_sp(self):
        """ A = SP """
        self.a_command('SP')                       # @SP
        self.c_destination('A', 'M')               # A = SP

    def offset_sp(self, i):
        """ D = SP - i """
        self.a_command(i)                          # A = i
        self.c_destination('D', 'A')               # D = A
        self.a_command("R0")
        self.c_destination('A', 'M')               # A = R0
        self.c_destination('D', 'A-D')             # D = A - D

# *****************************************************************************************


# **************** Generator commands. ****************************************************
    def a_command(self, value):
        """Returns @value."""
        self.out_file.write('@' + value + '\n')

    def c_destination(self, dest, comp):
        """Returns dest=comp."""
        self.out_file.write(dest + '=' + comp + '\n')

    def c_jump(self, comp, jump):
        """Returns comp;jump."""
        self.out_file.write(comp + ';' + jump + '\n')

    def l_command(self, label):
        """Returns (label)."""
        self.out_file.write('(' + label + ')\n')

    def new_label(self):
        self.count += 1
        return 'LABEL' + str(self.count)
# *****************************************************************************************

input_file_name = '/Users/wen/github/Nand2tetris/nand2tetris/projects/07/MemoryAccess/StaticTest/StaticTest.vm'
file_name, ext = os.path.splitext('/Users/wen/github/Nand2tetris/nand2tetris/projects/07/MemoryAccess/StaticTest/StaticTest.vm')
out_file_name = file_name + '.asm'

writer = CodeWriter(out_file_name)


parser = Parser(input_file_name)
while parser.advance():
    command_type = parser.command_type()
    if command_type in [C_POP, C_PUSH]:
        writer.write_push_pop(command_type, parser.arg1(), parser.arg2())
    elif command_type in [C_ARITHMETIC]:
        writer.write_arithmetic(parser.arg1())

