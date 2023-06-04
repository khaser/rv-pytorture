from Abstract import random_biased_xlen
from Config import Config
import ProcDriver as proc

class Test:
    name = 1

    def __init__(self, generator, test_name = None):
        self.gen = generator()
        self.mutate_data()
        if (test_name != None):
            self.name = test_name

    def mutate_data(self):
        xlen = Config.arch.value
        prefix = ".dword" if xlen == 64 else ".word"
        self.reg_init_bytes = '\n'.join(f"{prefix} {random_biased_xlen():#0{xlen//4 + 2}x}" for _ in range(32))
        self._get_name()

    def _get_name(self):
        self.name = "unnamed" + f'{Test.name:04}'
        Test.name += 1

    def run(self):
        proc.run_test(self.name, str(self))

    def __str__(self):
        reg_init_data = self.reg_init_bytes
        xlen = Config.arch.value

        load_regs = '\n'.join(f'  {"lw" if xlen == 32 else "ld"} x{i}, {4 * i}(x31)' for i in range(32))
        store_regs = '\n'.join(f'  {"sw" if xlen == 32 else "sd"} x{i}, {4 * i}(x31)' for i in range(31))

        test_text = str(self.gen)

        test_section = '\n'.join('  ' + cmd.strip() for cmd in test_text.split('\n'))

        return f'''
#include "riscv_macros.h"

{"RVTEST_RV32U" if xlen == 32 else "RVTEST_RV64U"}
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
{reg_init_data}

RVTEST_DATA_BEGIN
.align 8
test_memory: .space {Config.data_size}, 0
.align 8
xreg_dump_data: .space 32*{Config.arch.value // 4}, 0
RVTEST_DATA_END
'''

class TestSuite:
    def __init__(self, tests):
        self.tests = tests
        self.total_coverage = None
        self.rank = None

    def run(self):
        proc.clean_tmp()
        for test in self.tests:
            test.run()

        self.total_coverage = 0
        self.rank = dict()
        for covered, rank, _, test_name in proc.get_rank():
            self.total_coverage += covered
            self.rank[test_name] = 10**9 if rank == 0 else rank

    def retain_more_valuable(self, n):
        self.tests = sorted(self.tests, key = lambda test : self.rank[test.name])[:n]
