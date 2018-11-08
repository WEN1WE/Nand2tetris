from Constant import *


class Parser:
    """Handles the parsing of a single .vm file, and encapsulates access to the input code."""
    _command_type = {'add': C_ARITHMETIC,
                     'sub': C_ARITHMETIC,
                     'neg': C_ARITHMETIC,
                     'eq': C_ARITHMETIC,
                     'gt': C_ARITHMETIC,
                     'lt': C_ARITHMETIC,
                     'and': C_ARITHMETIC,
                     'or': C_ARITHMETIC,
                     'not': C_ARITHMETIC,
                     'label': C_LABEL,
                     'goto': C_GOTO,
                     'if-goto': C_IF,
                     'push': C_PUSH,
                     'pop': C_POP,
                     'call': C_CALL,
                     'return': C_RETURN,
                     'function': C_FUNCTION}

    def __init__(self, file):
        """Opens the input file."""
        self.commands = []
        for line in open(file, 'r').readlines():
            annotation = line.find('//')
            if annotation != -1:
                line = line[:annotation]
            if len(line) > 1:
                self.commands.append(line.strip().strip('\n').split())

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
        return Parser._command_type[self.command[0]]

    def arg1(self):
        """Returns the first arg."""
        if self.command_type() != C_RETURN:
            if self.command_type() == C_ARITHMETIC:
                return self.command[0]
            else:
                return self.command[1]

    def arg2(self):
        """Returns the second arg."""
        if self.command_type() in [C_PUSH, C_POP, C_FUNCTION, C_CALL]:
            return self.command[2]
