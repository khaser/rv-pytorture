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

def parse_rank(cmd):
    rank_run = subprocess.run(cmd, shell = True, stdout = subprocess.PIPE)
    output = rank_run.stdout.decode("utf-8")
    for test_line in output.strip().split('\n'):
        covered, rank, unique, test_name = test_line.split()
        yield int(covered), int(rank), int(unique), test_name


def random_biased_word():
    value = random.randint(0, 2**32 - 1)
    small = random.randint(0, 31)
    s = random.randint(0, 20)
    if s == 0:
        return small
    elif s == 1:
        return (0x80 + small) << 24 >> 24
    elif s == 2:
        return (0x8000 + small) << 16 >> 16
    elif s == 3:
        return (0x800000 + small) << 8 >> 8
    elif s == 4:
        return 0x80000000 + small
    elif s == 5:
        return (1 << small)
    elif s == 6:
        return (1 << 32) - (1 + (1 << small))
    else:
        return value

