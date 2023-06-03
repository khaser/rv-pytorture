import random
from Config import Config
from copy import deepcopy

class State:
    # [min_addr, max_addr]
    regs = set([f'x{i}' for i in range(1, 32)])

    def __init__(self, min_addr, max_addr, loop_limit, free_regs = None, funcs = []):
        self.min_addr = min_addr
        self.max_addr = max_addr
        self.loop_limit = loop_limit
        self.free_regs = free_regs if free_regs != None else State.regs
        self.funcs = funcs

    def random_reg(self, free=False, avoid_zeros=False):
        regs = self.free_regs if free else State.regs
        return random.choice(list(regs if avoid_zeros else regs | set(['x0'])))

    def random_imm(self, sz=8, neg=True):
        bound = 2 ** (sz - 1)
        return random.randint(-bound, bound - 1) if neg else random.randint(0, bound * 2 - 1)

    def random_addr(self, data_size=0):
        align = Config.arch.value // 8
        return f"test_memory + {random.randint(0, data_size // align - 1) * align}"

    def random_fun(self):
        suitable = [(func, ra) for func, ra, func_regs in self.funcs if ra in self.free_regs and func_regs <= self.free_regs]
        return random.choice(suitable)

    # TODO: rewrite to reflections?
    def copy(self, min_addr = None, max_addr = None, loop_limit = None, free_regs = None, funcs = None):
        new = deepcopy(self)
        if (min_addr != None):
            new.min_addr = min_addr
        if (max_addr != None):
            new.max_addr = max_addr
        if (loop_limit != None):
            new.loop_limit = loop_limit
        if (free_regs != None):
            new.free_regs = free_regs
        if (funcs != None):
            new.funcs = funcs
        return new

    def __len__(self):
        return self.max_addr - self.min_addr + 1
