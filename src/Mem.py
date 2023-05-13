from Abstract import *

class MemCommand(AbstractCommandType): 
    prefix = "xmem"

class StoreCommand(MemCommand):
    def __str__(self):
        return f"{self.cmd} {self.dest}, {self.addr}, {self.temp}"

    def __init__(self, config):
        self.cmd = random.choice(["sb", "sh", "sw"])
        while (1):
            self.dest = random_reg()
            self.temp = random_reg(avoid_zeros=True)
            self.addr = random_addr(config.data_size)
            if (self.dest != self.temp):
                break

class LoadCommand(MemCommand):
    def __str__(self):
        return f"{self.cmd} {self.dest}, {self.addr}"

    def __init__(self, config):
        self.cmd = random.choice(["lb", "lh", "lw", "lbu", "lhu"])
        self.dest, self.addr = random_reg(avoid_zeros=True), random_addr(config.data_size)

class SpecialLoad(MemCommand):
    def __str__(self):
        return f"{self.cmd} {self.dest}, {self.immediate}"

    def __init__(self, config):
        self.cmd = random.choice(["lui", "auipc"])
        self.dest, self.immediate = random_reg(), random_imm(20, False)

