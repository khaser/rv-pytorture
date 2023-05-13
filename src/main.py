#!/usr/bin/env python3.10

import os, sys, subprocess
import random

from Abstract import State, Config
from TestWriter import TestWriter
from Generators import RootGen

class Test:
    name = 1

    def __init__(self, config, generator, test_name = None):
        self.gen = generator
        self.config = config
        if (test_name == None):
            self.name = "unnamed" + str(Test.name)
            Test.name += 1
        else:
            self.name = test_name

    def __str__(self):
        return str(TestWriter(self.gen, self.config))
    
    def mutate(self):
        pass # TODO

    def run(self):
        subprocess.run("make mk_tmp", shell = True)
        filename = os.path.join(self.config.iteract_dir, f"{self.name}.S")
        print(str(self), file=open(filename, "w+"))

        res = subprocess.run(f"make PROG={self.name} run", shell = True)
        if res.returncode != 0:
            print(f"Signatures differ, {self.name}")
            exit(0)
 
class TestSuite:
    def __init__(self, size, config, state):
        self.tests = [Test(config, RootGen(config, state)) for _ in range(size)]
        self.total_coverage = None
        self.rank = None

    def run(self):
        subprocess.run("make rm_tmp", shell = True)
        for test in self.tests:
            test.run()
        rank_run = subprocess.run("make get_rank", shell = True, stdout = subprocess.PIPE)
        output = rank_run.stdout.decode("utf-8")

        self.total_coverage = 0
        self.rank = dict()
        for test_line in output.strip().split('\n'):
            covered, rank, _, test_name = test_line.split()
            print(covered, rank, test_name)
            covered, rank = int(covered), int(rank)
            self.total_coverage += covered
            self.rank[test_name] = 10**9 if rank == 0 else rank

    def most_valuable(self, n):
        return sorted(self.tests, key = lambda test : self.rank[test.name])[:n]

if __name__ == '__main__':
    _, config_filename, seed = sys.argv
    random.seed(seed)

    config = Config(open(sys.argv[1], 'r').readlines())
    state = State(0, 10)
    
    suite = TestSuite(10, config, state)
    suite.run()
    print([(x.name, suite.rank[x.name]) for x in suite.most_valuable(2)])
