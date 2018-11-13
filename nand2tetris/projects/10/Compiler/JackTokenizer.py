import re
from JackConstant import *


class JackTokenizer:
    """ """
    keywords_regex = '(?!\w)|'.join(keywords) + '(?!\w)'
    symbols_regex = '[' + re.escape('|'.join(symbols)) + ']'
    integer_regex = r'\d+'
    string_regex = r'"[^"\n]*"'
    identifier_regex = r'\w+'

    word_regex = re.compile(keywords_regex + '|' + symbols_regex + '|' + integer_regex + '|' + string_regex + '|' + identifier_regex)

    comment_regex = re.compile(r'//[^\n]*\n|/\*(.*?)\*/', re.MULTILINE | re.DOTALL)

    def __init__(self, file):
        """Opens the input file."""
        self.lines = open(file, 'r').read()
        self.tokens = JackTokenizer.tokenize(self.lines)
        self.index = -1
        self.token_type, self.token = (None, None)
        self.open_outfile(file)

    def has_more_commands(self):
        """Are there more commands in the input?"""
        return len(self.tokens) > self.index + 1

    def advance(self):
        """Reads the next command from the input and makes it the current command."""
        if self.has_more_commands():
            self.index += 1
            self.token_type, self.token = self.tokens[self.index]
            self.write_xml()
            return 1
        return 0

    def peek(self):
        return self.token_type, self.token

    def token_type(self):
        """Returns the type of the current token."""
        return self.token_type

    def key_word(self):
        """Returns the keyword which is the current token."""
        return self.token

    def symbol(self):
        """Returns the character which is the current token."""
        return self.token

    def identifier(self):
        """Returns the identifier which is the current token."""
        return self.token

    def int_val(self):
        """Returns the integer value of the current token."""
        return self.token

    def string_val(self):
        """Returns the string value of the current token."""
        return self.token

    def open_outfile(self, file):
        self.out_file = open(file.replace('.jack', 'TMY.xml'), 'w')
        self.out_file.write('<tokens>\n')

    def write_xml(self):
        token_type, token = self.token_type, self.token
        self.out_file.write('<' + tokens[token_type] + '> ')
        if token_type == KEYWORD:
            self.out_file.write(self.key_word())
        elif token_type == SYMBOL:
            self.out_file.write(self.symbol())
        elif token_type == INT_CONST:
            self.out_file.write(self.int_val())
        elif token_type == IDENTIFIER:
            self.out_file.write(self.identifier())
        elif token_type == STRING_CONST:
            self.out_file.write(self.string_val())
        self.out_file.write(' </' + tokens[token_type] + '>\n')

    def close_outfile(self):
        self.out_file.write('</tokens>')
        self.out_file.close()

    @staticmethod
    def split(line):
        return JackTokenizer.word_regex.findall(line)

    @staticmethod
    def token(word):
        if re.match(JackTokenizer.keywords_regex, word) is not None:
            return KEYWORD, word
        elif re.match(JackTokenizer.symbols_regex, word) is not None:
            return JackTokenizer.replace((SYMBOL, word))
        elif re.match(JackTokenizer.integer_regex, word) is not None:
            return INT_CONST, word
        elif re.match(JackTokenizer.string_regex, word) is not None:
            return STRING_CONST, word[1:-1]
        else:
            return IDENTIFIER, word

    @staticmethod
    def remove_comments(line):
        return JackTokenizer.comment_regex.sub('', line)

    @staticmethod
    def tokenize(lines):
        return [JackTokenizer.token(word) for word in JackTokenizer.split(JackTokenizer.remove_comments(lines))]

    @staticmethod
    def replace(pair):
        token_type, token = pair
        if token == '<':
            return token_type, '&lt;'
        elif token == '>':
            return token_type, '&gt;'
        elif token == '"':
            return token_type, '&quot;'
        elif token == '&':
            return token_type, '&amp;'
        else:
            return token_type, token
"""
file_name = '/Users/wen/github/Nand2tetris/nand2tetris/projects/10/ExpressionLessSquare/SquareGame.jack'
s = JackTokenizer(file_name)
s.open_outfile(file_name)
while s.advance:
    s.write_xml()
s.close_outfile()
"""




