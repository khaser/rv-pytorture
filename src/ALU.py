import random 

class ALUCommand: 
    def __init__(self, regs):
        self.dest, self.s1, self.s2 = regs
        self.cmd = None

    def __str__(self):
        return f"{self.cmd} {self.dest}, {self.s1}, {self.s2}"

    @staticmethod
    def random_command():
        command_class = random.choice(ALUCommand.__subclasses__())
        return command_class()

class AddCommand(ALUCommand):
    def __init__(self, *regs):
        super().__init__((regs))
        self.cmd = "add"

