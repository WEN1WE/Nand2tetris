from JackConstant import *


class SymbolTable:
    def __init__(self):
        """ """
        self.global_symbol = {}
        self.subroutine_symbol = {}
        self.symbols = {STATIC: self.global_symbol, FILED: self.global_symbol, ARG: self.subroutine_symbol, VAR: self.subroutine_symbol}
        self.index = {STATIC: 0, FILED: 0, ARG: 0, VAR: 0}

    def start_subroutine(self):
        """Starts a new subroutine scope."""
        self.subroutine_symbol.clear()
        self.index[ARG] = self.index[VAR] = 0

    def define(self, name, type, kind):
        """Defines a new identifier of the given name, type, and kind, and assigns it a running index."""
        self.symbols[kind][name] = (type, kind, self.index[kind])
        self.index[kind] += 1

    def var_count(self, kind):
        """Returns the number of variables of the given kind already defined in the current scope."""
        return sum([i for name, (t, k, i) in self.symbols[kind].items() if k == kind])

    def kind_of(self, name):
        """Returns the kind of the named identifier in the current scope."""
        (type, kind, index) = self.look_up(name)
        return kind

    def type_of(self, name):
        """Returns the type of the named identifier in the current scope."""
        (type, kind, index) = self.look_up(name)
        return type

    def index_of(self, name):
        """Returns the index assigned to the named identifier."""
        (type, kind, index) = self.look_up(name)
        return index

    def look_up(self, name):
        if name in self.subroutine_symbol:
            return self.subroutine_symbol[name]
        elif name in self.global_symbol:
            return self.global_symbol[name]
        else:
            return None, None, None
