class CodeWriter:
    """Translate VM commands into Hack assembly code."""
    def __init__(self, out_file_name):
        """Opens the output file."""
        out_file = open(out_file_name, 'w')

    def set_file_name(self):
        """Informs the code writer that the translation of a new VM file is started."""

    def write_arithmetic(self):
        """Writes the assembly code that is the translation of the given arithmetic command."""

    def write_push_pop(self):
        """Write the assembly code that is the translation of the push or pop command."""

    def close(self):
        """Closes the output file."""

    def wirte_init(self):
        """Write the assembly code that the VM initialization."""

    def write_label(self):
        """Write the assembly code that is the translation of the label command."""

    def wirte_goto(self):
        """Write the assembly code that is the translation of the goto command."""

    def write_if(self):
        """Write the assembly code that is the translation of the if command."""

    def write_call(self):
        """Write the assembly code that is the translation of the call command."""

    def write_return(self):
        """Write the assembly code that is the translation of the return command."""

    def write_function(self):
        """Write the assembly code that is the translation of the function command."""
