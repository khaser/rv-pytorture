#!/usr/bin/env python3.10

import os, sys, subprocess
import random

from Abstract import State, Config
from TestWriter import TestWriter
from Generators import RootGen

class Test:
    test_id = 1

    def __init__(self, config, generator):
        self.gen = generator
        self.config = config
        self.test_id = Test.test_id
        Test.test_id += 1

    def __str__(self):
        return str(TestWriter(self.gen, self.config))

    def run(self):
        filename = os.path.join(self.config.iteract_dir, f"{self.test_id}.S")
        print(str(self), file=open(filename, "w"))

        res = subprocess.run(f"make PROG={self.test_id} run", shell = True)
        if res.returncode != 0:
            print(f"Signatures differ, {self.test_id}")
            exit(0)
 
class TestSuite:

    def __init__(self, size, config, state):
        self.tests = [Test(config, RootGen(config, state)) for _ in range(size)]

    def run(self):
        for test in self.tests:
            test.run()
        print(subprocess.run("make get_rank", shell = True))

if __name__ == '__main__':
    _, config_filename, seed = sys.argv
    random.seed(seed)

    config = Config(open(sys.argv[1], 'r').readlines())
    state = State(0, 10)
    
    TestSuite(10, config, state).run()
