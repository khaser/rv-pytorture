import sys
import random

class AbstractCommandType:
    @staticmethod
    def choices(config, n = 1):
        mixed = ((int(config.mix[cmd_type.prefix]), cmd_type) for cmd_type in AbstractCommandType.__subclasses__())
        # print(AbstractCommandType.__subclasses__(), mixed[0], file=sys.stderr)
        weights, cmd_types = zip(*mixed)
        return random.choices(cmd_types, weights, k=n)


regs = [f'x{i}' for i in range(32)]

def random_reg():
    return random.choice(regs)

def random_imm(sz=8):
    bound = 2 ** (sz - 1)
    return random.randint(-bound, bound - 1)

def random_addr(data_size=0):
    return f"test_memory + {random.randint(0, data_size // 8) * 8}"

