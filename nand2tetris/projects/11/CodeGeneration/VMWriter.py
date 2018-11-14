class VMWriter:
    def __init__(self):
        """"""
    def open_outfile(self, file):
        self.out_file = open(file.replace('.jack', '.vm'), 'w')

    def close_outfile(self):
        self.out_file.close()

    def write_push(self, segment, index):
        """Writes a VM push command."""
        self.write_vm_cmd('push', segment, index)

    def write_pop(self, segment, index):
        """Writes a VM pop command."""
        self.write_vm_cmd('pop', segment, index)

    def write_arithmetic(self, op):
        """Writes a VM arithmetic-logical command."""
        self.write_vm_cmd(op)

    def write_label(self, label):
        """Writes a VM label command."""
        self.write_vm_cmd('label', label)

    def write_goto(self, label):
        """Writes a VM goto command."""
        self.write_vm_cmd('goto', label)

    def write_if(self, label):
        """Writes a VM if-goto command."""
        self.write_vm_cmd('if-goto', label)

    def write_call(self, name, num_args):
        """Writes a VM call command."""
        self.write_vm_cmd('call', name, num_args)

    def write_function(self, name, num_locals):
        """Writes a VM function command."""
        self.write_vm_cmd('function', name, num_locals)

    def write_return(self):
        """Writes a VM return command."""
        self.write_vm_cmd('return')

    def write_vm_cmd(self, cmd, arg1='', arg2=''):
        self.out_file.write(cmd + ' ' + str(arg1) + ' ' + str(arg2) + '\n')