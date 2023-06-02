from Config import Config
import random, subprocess

class AbstractCommandType:
    @staticmethod
    def choices(n = 1):
        mixed = ((int(Config.mix[cmd_type.prefix]), cmd_type) for cmd_type in AbstractCommandType.__subclasses__())
        weights, cmd_types = zip(*mixed)
        return random.choices(cmd_types, weights, k=n)

    @classmethod
    def random_command(cls):
        command_class = random.choice(cls.__subclasses__())
        return command_class

def random_biased_xlen():
    xlen = Config.arch.value
    value = random.randint(0, 2**xlen - 1)
    small = random.randint(0, xlen - 1)
    s = random.randint(0, 20)
    if s == 0:
        return small
    elif s == 1:
        return (0x80 + small) << (xlen - 8) >> (xlen - 8)
    elif s == 2:
        return (0x8000 + small) << (xlen - 16) >> (xlen - 16)
    elif s == 3:
        return (0x800000 + small) << (xlen - 24) >> (xlen - 24)
    elif s == 4:
        return 0x80000000 + small
    elif s == 5:
        return (1 << small)
    elif s == 6:
        return (1 << xlen) - (1 + (1 << small))
    elif s == 7:
        return value if (xlen == 32) else 2**63 + small
    else:
        return value

