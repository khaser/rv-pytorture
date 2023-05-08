from Abstract import *

class MemCommand(AbstractCommandType): 
    prefix = "xmem"

class StoreCommand(MemCommand):
    def __str__(self):
        return f"sw {self.dest}, {self.addr}, {self.temp}"
        # return f'''
# auipc {self.temp}, {self.addr}[31:12] + {self.addr}[11]
# sw {self.dest}, {self.addr}[11:0]({self.temp})
        # '''

    def __init__(self, config):
        while (1):
            self.dest = random_reg()
            self.temp = random_reg(avoid_zeros=True)
            self.addr = random_addr(config.data_size)
            if (self.dest != self.temp):
                break

class LoadCommand(MemCommand):
    def __str__(self):
        return f"lw {self.dest}, {self.addr}"

    def __init__(self, config):
        self.dest, self.addr = random_reg(avoid_zeros=True), random_addr(config.data_size)

