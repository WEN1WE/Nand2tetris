from Parser import *
from Code import *
from SymbolTable import *
#import sys


def main():

    file_name = '/Users/wen/github/Nand2tetris/nand2tetris/projects/06/pong/Pong.asm'
    new_file_name = file_name[:file_name.rfind('.')] + '.hack'
    new_file = open(new_file_name, 'w')

    parser1 = Parser(file_name)
    parser2 = Parser(file_name)
    code = Code()
    table = SymbolTable()
    PC = 0
    begin = 16

    # For each label declaration(LABEL) that appears in the source code, add the pair<LABEL, n> to the symbol table.
    while parser1.advance():
        if parser1.command_type() == 'L_COMMAND':
            table.symbol_table[parser1.symbol()] = str(PC)
        else:
            PC += 1

    # March again through the source code, and process each line.
    while parser2.advance():
        if parser2.command_type() == 'L_COMMAND':
            continue
        symbol = parser2.symbol()
        if symbol:
            if not str.isdigit(symbol):
                if symbol in table.symbol_table:
                    symbol = table.symbol_table[symbol]
                else:
                    table.symbol_table[symbol] = str(begin)
                    symbol = str(begin)
                    begin += 1
            line = str('{:016b}'.format(int(symbol))) + '\n'
            new_file.write(line)
        else:
            line = '111' + code.comp(parser2.comp()) + code.dest(parser2.dest()) + code.jump(parser2.jump()) + '\n'
            new_file.write(line)


main()