import random

class BranchCommand:
    def __init__(self, addr_off, state):
        self.addr_off = addr_off
        self.cmd = random.choice(["beq", "bne", "blt", "bge", "bltu", "bgeu"])
        self.src1, self.src2 = (state.random_reg() for i in range(2))

    def __str__(self):
        return f'{self.cmd} {self.src1}, {self.src2}, {self.addr_off}'
