import random 
import sys

regs = [f'x{i}' for i in range(32)]

def random_reg():
    return random.choice(regs)

def random_imm(sz=8):
    bound = 2 ** (sz - 1)
    return random.randint(-bound, bound - 1)

def random_addr(data_size=0):
    return f"test_memory + {random.randint(0, data_size // 8) * 8}"

class MemCommand: 
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

