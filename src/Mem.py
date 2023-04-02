from Abstract import *

class MemCommand(AbstractCommandType): 
    prefix = "xmem"

    @staticmethod
    def random_command():
        command_class = random.choice(MemCommand.__subclasses__())
        return command_class

class StoreCommand(MemCommand):
    def __str__(self):
        return f"sw {self.dest}, {self.addr}, {self.temp}"

    def __init__(self, config):
        self.dest, self.temp = random.sample(regs, 2)
        self.addr = random_addr(config.data_size)

class LoadCommand(MemCommand):
    def __str__(self):
        return f"lw {self.dest}, {self.addr}"

    def __init__(self, config):
        self.dest, self.addr = random_reg(), random_addr(config.data_size)

