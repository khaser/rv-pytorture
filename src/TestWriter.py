from Mem import *
from ALU import *
from Branch import *

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
        return f'.align 8\ntest_memory: .space {self.config.data_size}, 0'

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
