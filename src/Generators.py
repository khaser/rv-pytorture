from Mem import *
from ALU import *
from Branch import *
from Abstract import Config
import copy
from itertools import accumulate

class SeqGen:
    min_sz = 1

    def __init__(self, config: Config, state: State):
        self.config = config
        self.state = state

    def __str__(self):
        n = self.state.max_addr - self.state.min_addr + 1
        return '\n'.join(str(cmd_type.random_command()(self.config, self.state))
                         for cmd_type in AbstractCommandType.choices(self.config, n))

class BranchGen:
    min_sz = 4

    def __init__(self, config: Config, state: State):
        self.config = config
        self.state = state

    def __str__(self):
        j_addr = random.randint(self.state.min_addr + 2, self.state.max_addr - 1)
        label = "if_" + str(self.state.min_addr)
        return '''
        {branch_statement}
        {else_block}
        j end{label} 
        {label}:
        {if_block}
        end{label}:
        '''.format(
                branch_statement = BranchCommand(label, self.state),
                else_block = RootGen(self.config, State(self.state.min_addr + 1, j_addr, self.state.free_regs)),
                if_block = RootGen(self.config, State(j_addr + 1, self.state.max_addr, self.state.free_regs)),
                label = label,
                )

class LoopGen:
    min_sz = 4

    def __init__(self, config: Config, state: State):
        self.config = config
        self.state = state

    def __str__(self):
        loop_counter = self.state.random_reg(free=True, avoid_zeros=True)
        new_state = copy.deepcopy(self.state)
        new_state.free_regs.remove(loop_counter)
        new_state.min_addr += 1
        new_state.max_addr -= 2
        return '''
        addi {loop_counter}, x0, {iterations}
        {label}:
        {for_block}
        addi {loop_counter}, {loop_counter}, -1
        bnez {loop_counter}, {label}
        '''.format(
                for_block = RootGen(self.config, new_state),
                label = "for_" + str(self.state.min_addr),
                iterations = random.randint(1, self.config.max_loop_iterations),
                loop_counter = loop_counter,
                )

class RootGen:
    def split(self, tl, tr):
        k = tr - tl
        res = []
        while k != 0:
            x = random.randint(1, k)
            k -= x
            res.append(x)
        random.shuffle(res)
        res = list(map(lambda x : tl + x, accumulate(res)))
        return res
        

    def __init__(self, config: Config, state = None):
        res = []
        self.state = state if state != None else config.initial_state 

        indices = self.split(self.state.min_addr, self.state.max_addr + 1)

        for fr, to in zip(indices[:-1], indices[1:]):
            block_len = to - fr
            if (block_len < config.only_seq_threshold):
                res.append(SeqGen(config, State(fr, to - 1, self.state.free_regs)))
            else:
                generators = [BranchGen, LoopGen]
                fitable_generators = list(filter(lambda Gen : Gen.min_sz <= block_len, generators))
                gen = random.choice(fitable_generators)
                res.append(gen(config, State(fr, to - 1, self.state.free_regs)))
        self.res = res
        

    def __str__(self):
        return '\n\n'.join(str(i) for i in self.res)
