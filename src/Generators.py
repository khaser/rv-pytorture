from Mem import *
from ALU import *
from Branch import *
from Abstract import Config

class SeqGen:
    def __init__(self, config: Config, state: State):
        self.config = config
        self.state = state

    def __str__(self):
        n = self.state.max_addr - self.state.min_addr + 1
        return '\n'.join(str(cmd_type.random_command()(self.config)) for cmd_type in AbstractCommandType.choices(self.config, n))

class BranchGen:
    def __init__(self, config: Config, state: State):
        self.config = config
        self.state = state

    def pick_gen(self, state):
        generator = SeqGen if len(state) < 5 else random.choice([SeqGen, BranchGen])
        return generator(self.config, state)

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
                branch_statement = BranchCommand(label),
                else_block = self.pick_gen(State(self.state.min_addr + 1, j_addr)),
                if_block = self.pick_gen(State(j_addr + 1, self.state.max_addr)),
                label = label,
                )

class RootGen:
    def __init__(self, config: Config):
        res = []
        state = config.initial_state 
        n = int(abs(random.normalvariate(1, (state.max_addr - state.min_addr +  1) ** 0.5))) + 1

        indices = random.sample(range(state.min_addr + 1, state.max_addr + 1), k=n)
        indices.extend([state.min_addr, state.max_addr + 1])
        indices.sort()
        for fr, to in zip(indices[:-1], indices[1:]):
            if (to - fr < 5):
                res.append(SeqGen(config, State(fr, to - 1)))
            else:
                res.append(BranchGen(config, State(fr, to - 1)))
        self.res = res
        

    def __str__(self):
        return '\n\n'.join(str(i) for i in self.res)
