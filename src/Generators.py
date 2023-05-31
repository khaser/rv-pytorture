from Mem import *
from ALU import *
from Branch import *
from Config import Config
from State import State
from itertools import accumulate

class SeqGen:
    min_sz = 1

    def __init__(self, state: State):
        self.state = state

    def __str__(self):
        n = self.state.max_addr - self.state.min_addr + 1
        return '\n'.join(str(cmd_type.random_command()(self.state))
                         for cmd_type in AbstractCommandType.choices(n))

class BranchGen:
    min_sz = 4

    def __init__(self, state: State):
        self.state = state

    def __str__(self):
        j_addr = random.randint(self.state.min_addr + 2, self.state.max_addr - 1)
        label = "if_" + str(self.state.min_addr)
        else_state = self.state.copy(min_addr = self.state.min_addr + 1, max_addr = j_addr - 1)
        if_state = self.state.copy(min_addr = j_addr + 1)
        return '''
        {branch_statement}
        {else_block}
        j end{label} 
        {label}:
        {if_block}
        end{label}:
        '''.format(
                branch_statement = BranchCommand(label, self.state),
                else_block = RootGen(else_state),
                if_block = RootGen(if_state),
                label = label,
                )

class LoopGen:
    min_sz = 4

    def __init__(self, state: State):
        self.state = state

    def __str__(self):
        loop_counter_reg = self.state.random_reg(free=True, avoid_zeros=True)
        new_state = self.state.copy(
                min_addr = self.state.min_addr + 1, 
                loop_limit = self.state.loop_limit - 1,
                free_regs = [x for x in self.state.free_regs if x != loop_counter_reg],
            )

        return '''
        addi {loop_counter_reg}, x0, {iterations}
        {label}:
        {for_block}
        addi {loop_counter_reg}, {loop_counter_reg}, -1
        bnez {loop_counter_reg}, {label}
        '''.format(
                for_block = RootGen(new_state),
                label = "for_" + str(self.state.min_addr),
                iterations = random.randint(1, Config.max_loop_iterations),
                loop_counter_reg = loop_counter_reg,
                )

class FunctionDefGen:
    min_sz = 4

    def __init__(self, state: State):
        self.state = state

    def __str__(self):
        ra_reg = self.state.random_reg(free=True, avoid_zeros=True)
        j_addr = random.randint(self.state.min_addr + 2, self.state.max_addr - 1)
        func_name = "fun_" + str(self.state.min_addr)

        fun_state = self.state.copy(
                min_addr = self.state.min_addr + 1,
                max_addr = j_addr - 1,
                free_regs = [x for x in self.state.free_regs if x != ra_reg],
            ) 
        cont_state = self.state.copy(
                min_addr = j_addr + 1,
                funcs = self.state.funcs + [(func_name, ra_reg)],
            ) 

        return '''
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

class FunctionCallGen:
    min_sz = 2

    def __init__(self, state: State):
        self.state = state

    def __str__(self):
        fun_label, ra_reg = self.state.random_fun()

        self.state.free_regs.remove(ra_reg)
        tmp_reg = self.state.random_reg(free=True, avoid_zeros=True)
        self.state.free_regs.append(ra_reg)

        cont_state = self.state.copy(min_addr = self.state.min_addr + 2)
        continuation = RootGen(cont_state)

        return f'''
            la {tmp_reg}, {fun_label}
            jalr {ra_reg}, {tmp_reg}, 0
            {continuation}
        '''

class RootGen:
    def __init__(self, state = None):
        self.res = []
        self.state = state if state != None else Config.initial_state 

        indices = self.split(self.state.min_addr, self.state.max_addr + 1)

        for fr, to in zip(indices[:-1], indices[1:]):
            block_state = self.state.copy(min_addr = fr, max_addr = to - 1)
            fitable_generators = self.select_suitable(block_state)
            gen = random.choice(fitable_generators)
            self.res.append(gen(block_state))

    def select_suitable(self, state):
        block_len = state.max_addr - state.min_addr

        if (block_len < Config.only_seq_threshold):
            return [ SeqGen ]

        generators = [BranchGen, FunctionDefGen]

        assert state.loop_limit >= 0
        if state.loop_limit != 0:
            generators.append(LoopGen)
        
        if len(state.free_regs) >= 2 and any(ra in state.free_regs for _, ra in state.funcs) > 0:
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
        return '\n\n'.join(str(i) for i in self.res)
