from Abstract import Config, parse_rank
import os, subprocess

class Test:
    name = 1

    def __init__(self, config, test_name = None):
        self.gen = config.generator
        self.config = config
        self.reg_init_bytes = os.urandom(32 * 4)
        if (test_name == None):
            self.name = "unnamed" + f'{Test.name:04}'
            Test.name += 1
        else:
            self.name = test_name

    def mutate_data(self):
        self.reg_init_bytes = os.urandom(32 * 4)

    def run(self):
        subprocess.run("make mk_tmp -s", shell = True)
        filename = os.path.join(self.config.iteract_dir, f"{self.name}.S")
        print(str(self), file=open(filename, "w+"))

        res = subprocess.run(f"make PROG={self.name} run", shell = True)
        if res.returncode != 0:
            print(f"Signatures differ, {self.name}")
            exit(0)

    def __str__(self):
        reg_init_data = '\n'.join(f".word 0x{self.reg_init_bytes[i:i+4].hex()}" for i in range(0, len(self.reg_init_bytes), 4))

        load_regs = '\n'.join(f"  lw x{i}, {4 * i}(x31)" for i in range(32))
        store_regs = '\n'.join(f"  sw x{i}, {4 * i}(x31)" for i in range(31))

        test_text = str(self.gen(self.config))

        test_section = '\n'.join('  ' + cmd.strip() for cmd in test_text.split('\n'))

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
{reg_init_data}

RVTEST_DATA_BEGIN
.align 8
test_memory: .space {self.config.data_size}, 0
.align 8
xreg_dump_data: .space 32*4, 0
RVTEST_DATA_END
'''

class TestSuite:
    def __init__(self, tests):
        self.tests = tests
        self.total_coverage = None
        self.rank = None

    def run(self):
        subprocess.run("make rm_tmp", shell = True)
        for test in self.tests:
            test.run()

        self.total_coverage = 0
        self.rank = dict()
        for covered, rank, _, test_name in parse_rank("make get_rank"):
            self.total_coverage += covered
            self.rank[test_name] = 10**9 if rank == 0 else rank

    def retain_more_valuable(self, n):
        self.tests = sorted(self.tests, key = lambda test : self.rank[test.name])[:n]
