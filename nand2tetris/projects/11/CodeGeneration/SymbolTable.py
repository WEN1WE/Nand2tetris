class SymbolTable:
    def __init__(self):
        """ """

    def start_subroutine(self):
        """Start a new subroutine scope."""

    def define(self):
        """Defines a new identifier of the given name, type, and kind, and assigns it a running index."""

    def var_count(self):
        """Returns the number of variables of the given kind already defined in the current scope."""

    def kind_of(self):
        """Returns the kind of the named identifier in the current scope."""

    def type_of(self):
        """Returns the type of the named identifier in the current scope."""

    def index_of(self):
        """Returns the index assigned to the named identifier."""

