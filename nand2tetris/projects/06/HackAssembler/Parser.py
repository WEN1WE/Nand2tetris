"""Encapsulates access to the input code."""
class Parser:
    # Opens the input file.
    def __init__(self, filename):
        self.commands = [line.strip('\n') for line in open(filename).readlines() if not line.startswith('//') and len(line) > 1]
        self.index = -1
        self.command = None

    # Are there more commands in the input?
    def hasMoreCommands(self):
        return len(self.command) != self.index

    # Reads the next command from the input and makes it the current command.
    def advance(self):
        self.index += 1
        if self.hasMoreCommands():
            self.command = self.command[self.index]

    # Returns the type of the current command.
    def commandType(self):
        if self.command.startswith('@'):
            return 'A_COMMAND'
        elif self.command.startswith('('):
            return 'L_COMMAND'
        else:
            return 'C_COMMAND'

    # Returns the symbol or decimal Xxx.
    def symbol(self):
        if self.commandType() == 'A_COMMAND' or 'L_COMMAND':
            return self.command.strip('()@')

    # Returns the dest mnemonic in the current C-command.
    def dest(self):
        if self.commandType() == 'C_COMMAND' and self.command.find('=') != -1:
            return self.command[0:self.command.find('=')]

    # Returns the comp mnemonic in the current C-command.
    def comp(self):
        if self.commandType() == 'C_COMMAND' and self.command.find('=') != -1:
            return self.command[self.command.find('=')+1:]

    # Return the jump mnemonic in the current C-command.
    def jump(self):
        return self.command



a = 'abc=123'
print(a[a.find('=')+1:])







