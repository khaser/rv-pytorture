from Mem import *
from ALU import *
from Branch import *
from Config import Config
from State import State
from itertools import accumulate
import random

class SeqGen:
    sname = 'seq'
    min_sz = 1

    def __init__(self, state: State):
        n = state.max_addr - state.min_addr + 1
        self.res = '\n'.join(str(cmd_type.random_command()(state))
                         for cmd_type in AbstractCommandType.choices(n))

    def __str__(self):
        return self.res

class BranchGen:
    min_sz = 4
    sname = 'branch'

    def __init__(self, state: State):
        j_addr = random.randint(state.min_addr + 2, state.max_addr - 1)
        label = "if_" + str(state.min_addr)
        else_state = state.copy(min_addr = state.min_addr + 1, max_addr = j_addr - 1)
        if_state = state.copy(min_addr = j_addr + 1)
        self.res = '''
        {branch_statement}
        {else_block}
        j end{label} 
        {label}:
        {if_block}
        end{label}:
        '''.format(
                branch_statement = BranchCommand(label, state),
                else_block = RootGen(else_state),
                if_block = RootGen(if_state),
                label = label,
                )

    def __str__(self):
        return self.res

class LoopGen:
    min_sz = 4
    sname = 'loop'

    def __init__(self, state: State):
        loop_counter_reg = state.random_reg(free=True, avoid_zeros=True)
        new_state = state.copy(
                min_addr = state.min_addr + 1, 
                loop_limit = state.loop_limit - 1,
                free_regs = state.free_regs - set([loop_counter_reg])
            )

        self.res = '''
        addi {loop_counter_reg}, x0, {iterations}
        {label}:
        {for_block}
        addi {loop_counter_reg}, {loop_counter_reg}, -1
        bnez {loop_counter_reg}, {label}
        '''.format(
                for_block = RootGen(new_state),
                label = "for_" + str(state.min_addr),
                iterations = random.randint(1, Config.max_loop_iterations),
                loop_counter_reg = loop_counter_reg,
                )

    def __str__(self):
        return self.res

class FunctionDefGen:
    min_sz = 4
    sname = 'func_def'

    def __init__(self, state: State):
        ra_reg = state.random_reg(free=True, avoid_zeros=True)
        other_free =  state.free_regs - set([ra_reg])
        regs_for_func = set(random.sample(other_free, k = random.randint(0, len(other_free))))

        j_addr = random.randint(state.min_addr + 2, state.max_addr - 1)
        func_name = "fun_" + str(state.min_addr)

        fun_state = state.copy(
                min_addr = state.min_addr + 1,
                max_addr = j_addr - 1,
                free_regs = regs_for_func,
            ) 
        cont_state = state.copy(
                min_addr = j_addr + 1,
                funcs = state.funcs + [(func_name, ra_reg, state.free_regs - regs_for_func)],
            ) 

        self.res = '''
        j end{label}
        {label}:
        {function_body}
        jalr x0, {ra_reg}, 0
        end{label}:
        {continuation}
        '''.format(
                ra_reg = ra_reg,
                label = func_name,
                continuation = RootGen(cont_state),
                function_body = RootGen(fun_state),
            )

    def __str__(self):
        return self.res

class FunctionCallGen:
    min_sz = 2
    sname = 'func_call'

    def __init__(self, state: State):
        fun_label, ra_reg = state.random_fun()

        state.free_regs.remove(ra_reg)
        tmp_reg = state.random_reg(free=True, avoid_zeros=True)
        state.free_regs.add(ra_reg)

        cont_state = state.copy(min_addr = state.min_addr + 2)
        continuation = RootGen(cont_state)

        self.res = f'''
            la {tmp_reg}, {fun_label}
            jalr {ra_reg}, {tmp_reg}, 0
            {continuation}
        '''

    def __str__(self):
        return self.res

class RootGen:
    def __init__(self, state = None):
        self.res = []
        self.state = state if state != None else State(0, Config.test_size, Config.max_loop_nesting)

        indices = self.split(self.state.min_addr, self.state.max_addr + 1)

        for fr, to in zip(indices[:-1], indices[1:]):
            block_state = self.state.copy(min_addr = fr, max_addr = to - 1)
            fitable_generators = self.select_suitable(block_state)
            gen = random.choices(fitable_generators, k=1, weights=[Config.pattern_mix[gen.sname] for gen in fitable_generators])[0]
            self.res.append(gen(block_state))

    def select_suitable(self, state):
        block_len = state.max_addr - state.min_addr

        if (block_len < Config.only_seq_threshold):
            return [ SeqGen ]

        generators = [BranchGen, FunctionDefGen]

        assert state.loop_limit >= 0
        if state.loop_limit != 0:
            generators.append(LoopGen)
        
        if len(state.free_regs) >= 2 and any(ra in state.free_regs and func_regs <= state.free_regs for _, ra, func_regs in state.funcs) > 0:
            generators.append(FunctionCallGen)

        return [gen for gen in generators if gen.min_sz <= block_len]
        
    def split(self, tl, tr):
        k = tr - tl
        res = [0]
        while k != 0:
            x = random.randint(1, k)
            k -= x
            res.append(x)
        random.shuffle(res)
        res = list(map(lambda x : tl + x, accumulate(res)))
        return res

    def __str__(self):
        return '\n'.join(str(i) for i in self.res)
