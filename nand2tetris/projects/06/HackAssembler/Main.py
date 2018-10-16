from Parser import *
from Code import *
from SymbolTable import *
#import sys


def main():
    file_name = '/Users/wen/github/Nand2tetris/nand2tetris/projects/06/add/Add.asm'
    new_file_name = file_name[:file_name.rfind('.')] + '.hack'
    new_file = open(new_file_name, 'w')

    parser = Parser(file_name)
    code = Code()
    symbol_table = SymbolTable()

    while parser.advance():
        symbol = parser.symbol()
        if symbol:
            line = str(bin(int(symbol))) + '\n'
            new_file.write(line)
        else:
            line = '111' + code.comp(parser.comp()) + code.dest(parser.dest()) + code.jump(parser.jump()) + '\n'
            new_file.write(line)

main()
print(1)



