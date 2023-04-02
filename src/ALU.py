from Abstract import *
import random 

class ALUCommand(AbstractCommandType): 
    prefix = "xalu"

class AddCommand(ALUCommand):
    def __str__(self):
        return f"add {self.dest}, {self.src1}, {self.src2}"

    def __init__(self, config):
        self.dest, self.src1, self.src2 = (random_reg() for i in range(3))

