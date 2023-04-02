from Abstract import *

class MemCommand(AbstractCommandType): 
    prefix = "xmem"

class StoreCommand(MemCommand):
    def __str__(self):
        return f"sw {self.dest}, {self.addr}, {self.temp}"

    def __init__(self, config):
        self.dest = random_reg()
        self.temp = random_reg(avoid_zeros=True)
        self.addr = random_addr(config.data_size)

class LoadCommand(MemCommand):
    def __str__(self):
        return f"lw {self.dest}, {self.addr}"

    def __init__(self, config):
        self.dest, self.addr = random_reg(avoid_zeros=True), random_addr(config.data_size)

