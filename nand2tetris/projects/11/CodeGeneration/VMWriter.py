class VMWriter:
    def __init__(self):
        """"""

    def write_push(self):
        """Writes a VM push command."""

    def write_pop(self):
        """Writes a VM pop command."""

    def write_arithmetic(self):
        """Writes a VM arithmetic-logical command."""

    def write_label(self):
        """Writes a VM label command."""

    def write_goto(self):
        """Writes a VM goto command."""

    def write_if(self):
        """Writes a VM if-goto command."""

    def write_call(self):
        """Writes a VM call command."""

    def write_function(self):
        """Writes a VM function command."""

    def write_return(self):
        """Writes a VM return command."""

    def write_close(self):
        """Closes the output file."""