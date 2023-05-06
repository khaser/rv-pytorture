import sys
import random

class AbstractCommandType:
    @staticmethod
    def choices(config, n = 1):
        mixed = ((int(config.mix[cmd_type.prefix]), cmd_type) for cmd_type in AbstractCommandType.__subclasses__())
        weights, cmd_types = zip(*mixed)
        return random.choices(cmd_types, weights, k=n)

    @classmethod
    def random_command(cls):
        command_class = random.choice(cls.__subclasses__())
        return command_class


regs = [f'x{i}' for i in range(1, 32)]

def random_reg(avoid_zeros=False):
    return random.choice(regs if avoid_zeros else regs + ['x0'])

def random_imm(sz=8):
    bound = 2 ** (sz - 1)
    return random.randint(-bound, bound - 1)

def random_addr(data_size=0):
    return f"test_memory + {random.randint(0, data_size // 8 - 1) * 8}"

