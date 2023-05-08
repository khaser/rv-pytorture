#!/usr/bin/env python3.10

import os, sys
import random

from Abstract import AbstractCommandType
from Mem import *
from ALU import *
from Branch import *

class State:
    # [min_addr, max_addr]
    def __init__(self, min_addr, max_addr):
        self.min_addr = min_addr
        self.max_addr = max_addr

class Config:
    def __init__(self, lines):
        # TODO: inform about ignored options
        def take_prefix(lines, prefix):
            return (line[len(prefix):] for line in lines if line.startswith(prefix))

        lines = take_prefix(lines, 'torture.generator.')
        self.mix = dict(tuple(line.strip().split()) for line in take_prefix(lines, 'mix.'))

        self.data_size = 2**6 # TODO

class TestWriter:
    def __init__(self, commands, config):
        self.commands = commands
        self.config = config

    def reg_init(self):
        load_regs = '\n'.join(f"  lw x{i}, {4 * i}(x31)" for i in range(32))
        return f'''
xreg_init:
  la x31, xreg_init_data
{load_regs}
        '''
  
    def reg_dump(self):
        load_regs = '\n'.join(f"  sw x{i}, {4 * i}(x31)" for i in range(31))
        return f'''
xreg_dump:
  la x31, xreg_dump_data
{load_regs}
        '''

    def reg_init_data(self):
        data = '\n'.join(f".word {hex(random.randint(0, 2**32))}" for i in range(32))
        return f'''
xreg_init_data:
{data}
'''
    def reg_dump_data(self):
        return f'.align 8\nxreg_dump_data: .space 32*4, 0'

    def test_memory_data(self):
        return f'.align 8\ntest_memory: .space {config.data_size}, 0'

    def __str__(self):
        test_section = '\n'.join('  ' + cmd.strip() for cmd in str(self.commands).split('\n'))
        not_dumped_data = self.reg_init_data() 
        dumped_data = '\n'.join([self.test_memory_data(), self.reg_dump_data()])
        return f'''
#include "riscv_macros.h"

RVTEST_RV32U
RVTEST_CODE_BEGIN

{self.reg_init()}
test_body:{test_section}
{self.reg_dump()}

RVTEST_PASS

RVTEST_CODE_END

.data
{not_dumped_data}
RVTEST_DATA_BEGIN
{dumped_data}
RVTEST_DATA_END
'''

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
                else_block = SeqGen(self.config, State(self.state.min_addr + 1, j_addr)),
                if_block = SeqGen(self.config, State(j_addr + 1, self.state.max_addr)),
                label = label,
                )

class RootGen:
    def __init__(self, config: Config, state: State):
        res = []
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


if __name__ == '__main__':
    _, config_filename, seed = sys.argv
    random.seed(seed)

    config = Config(open(sys.argv[1], 'r').readlines())

    print(TestWriter(RootGen(config, State(0, 10)), config))
