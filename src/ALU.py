from Abstract import *
import random 

class ALUCommand(AbstractCommandType): 
    prefix = "xalu"

class ALURtype(ALUCommand):
    def __str__(self):
        return f"{self.cmd} {self.dest}, {self.src1}, {self.src2}"

    def __init__(self, config):
        self.cmd = random.choice(["add", "slt", "sltu", "and", "or", "xor", "sll", "srl", "sub", "sra"])
        self.dest, self.src1, self.src2 = (random_reg() for i in range(3))

class ALUItype(ALUCommand):
    def __str__(self):
        return f"{self.cmd} {self.dest}, {self.src}, {self.immediate}"

    def __init__(self, config):
        shifts = ["slli", "srli", "srai"]
        self.cmd = random.choice(["addi", "slti", "sltiu", "andi", "ori", "xori"] + shifts)
        self.dest, self.src = random_reg(), random_reg() 
        self.immediate = random_imm(5 if self.cmd in shifts else 12, self.cmd not in shifts)
