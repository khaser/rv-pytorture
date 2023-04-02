from Abstract import *
import random 

class ALUCommand(AbstractCommandType): 
    prefix = "xalu"

    @staticmethod
    def random_command():
        command_class = random.choice(ALUCommand.__subclasses__())
        return command_class

class AddCommand(ALUCommand):
    def __str__(self):
        return f"add {self.dest}, {self.src1}, {self.src2}"

    def __init__(self, config):
        self.dest, self.src1, self.src2 = (random_reg() for i in range(3))

