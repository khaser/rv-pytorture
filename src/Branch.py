from Abstract import random_reg
import random 

class BranchCommand: 
    def __init__(self, addr_off):
        self.addr_off = addr_off
        self.src1, self.src2 = (random_reg() for i in range(2))

    def __str__(self):
        bcmd = random.choice(["beq", "bne", "blt", "bge"])
        return f'{bcmd} {self.src1}, {self.src2}, {self.addr_off}'
