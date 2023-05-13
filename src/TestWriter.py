from Mem import *
from ALU import *
from Branch import *

class TestWriter:
    def __init__(self, config, commands, reg_init_bytes):
        self.commands = commands
        self.config = config
        self.reg_init_data = '\n'.join(f".word 0x{reg_init_bytes[i:i+4].hex()}" for i in range(0, len(reg_init_bytes), 4))
  
    def reg_dump_data(self):
        return f''

    def __str__(self):
        load_regs = '\n'.join(f"  lw x{i}, {4 * i}(x31)" for i in range(32))
        store_regs = '\n'.join(f"  sw x{i}, {4 * i}(x31)" for i in range(31))

        test_section = '\n'.join('  ' + cmd.strip() for cmd in str(self.commands).split('\n'))

        return f'''
#include "riscv_macros.h"

RVTEST_RV32U
RVTEST_CODE_BEGIN

xreg_init:
  la x31, xreg_init_data
{load_regs}

test_body:{test_section}

xreg_dump:
  la x31, xreg_dump_data
{store_regs}

RVTEST_PASS

RVTEST_CODE_END

.data
xreg_init_data:
{self.reg_init_data}

RVTEST_DATA_BEGIN
.align 8
test_memory: .space {self.config.data_size}, 0
.align 8
xreg_dump_data: .space 32*4, 0
RVTEST_DATA_END
'''
