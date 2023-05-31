from Abstract import AbstractCommandType
import random
from Config import Config

class MemCommand(AbstractCommandType): 
    prefix = "xmem"

class StoreCommand(MemCommand):
    def __str__(self):
        return f"{self.cmd} {self.dest}, {self.addr}, {self.temp}"

    def __init__(self, state):
        self.cmd = random.choice(["sb", "sh", "sw"])
        while (1):
            self.dest = state.random_reg()
            self.temp = state.random_reg(free=True, avoid_zeros=True)
            self.addr = state.random_addr(Config.data_size)
            if (self.dest != self.temp):
                break

class LoadCommand(MemCommand):
    def __str__(self):
        return f"{self.cmd} {self.dest}, {self.addr}"

    def __init__(self, state):
        self.cmd = random.choice(["lb", "lh", "lw", "lbu", "lhu"])
        self.dest, self.addr = state.random_reg(free=True, avoid_zeros=True), state.random_addr(Config.data_size)

class SpecialLoad(MemCommand):
    def __str__(self):
        return f"{self.cmd} {self.dest}, {self.immediate}"

    def __init__(self, state):
        self.cmd = random.choice(["lui", "auipc"])
        self.dest, self.immediate = state.random_reg(free=True), state.random_imm(20, False)

