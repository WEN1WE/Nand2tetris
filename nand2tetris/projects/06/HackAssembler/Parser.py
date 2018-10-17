class Parser:
    """Encapsulates access to the input code."""

    def __init__(self, file):
        """Opens the input file."""
        self.commands = []
        for line in open(file, 'r').readlines():
            annotation = line.find('//')
            if annotation != -1:
                line = line[:annotation]
            if len(line) > 1:
                self.commands.append(line.strip().strip('\n'))

        self.index = -1
        self.command = None

    def has_more_commands(self):
        """Are there more commands in the input?"""
        return len(self.commands) > self.index + 1

    def advance(self):
        """Reads the next command from the input and makes it the current command."""
        if self.has_more_commands():
            self.index += 1
            self.command = self.commands[self.index]
            return 1
        return 0

    def command_type(self):
        """Returns the type of the current command."""
        if self.command.startswith('@'):
            return 'A_COMMAND'
        elif self.command.startswith('('):
            return 'L_COMMAND'
        else:
            return 'C_COMMAND'

    def symbol(self):
        """Returns the symbol or decimal Xxx."""
        command_type = self.command_type()
        if command_type == 'A_COMMAND' or command_type == 'L_COMMAND':
            return self.command.strip('()@')
        else:
            return None

    def dest(self):
        """Returns the dest mnemonic in the current C-command."""
        if self.command_type() == 'C_COMMAND' and self.command.find('=') != -1:
            return self.command[0:self.command.find('=')]
        else:
            return 'null'

    def comp(self):
        """Returns the comp mnemonic in the current C-command."""
        if self.command_type() == 'C_COMMAND':
            if self.command.find('=') != -1:
                return self.command[self.command.find('=')+1:]
            else:
                return self.command[:self.command.find(';')]

    def jump(self):
        """Return the jump mnemonic in the current C-command."""
        if self.command.find(';') != -1:
            return self.command[self.command.find(';')+1:]
        else:
            return 'null'




#parser = Parser('/Users/wen/github/Nand2tetris/nand2tetris/projects/06/max/Max.asm')
#print(parser.commands)







