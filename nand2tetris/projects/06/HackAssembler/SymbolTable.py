class SymbolTable:
    """A symbol table that keeps a correspondence between symbolic labels and numeric addresses."""
    def __init__(self):
        self.symbolTable = {}

    def add_entry(self, symbol, address):
        """Adds the pair(symbol, address) to the table."""
        self.symbolTable[symbol] = address

    def contains(self, symbol):
        """Does the symbol table contain the given symbol?"""
        return symbol in self.symbolTable

    def get_address(self, symbol):
        """Returns the address associated with the symbol."""
        return self.symbolTable[symbol]
