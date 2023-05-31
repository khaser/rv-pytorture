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


