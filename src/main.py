#!/usr/bin/env python3.10

import sys, random

from Runners import TestSuite, Test
from Generators import RootGen
from Config import Config
import ProcDriver as proc

if __name__ == '__main__':
    _, seed = sys.argv
    random.seed(seed)

    generations = Config.generations
    tests_in_generation = Config.tests_in_generation
    retain_to_next_gen = Config.retain_to_next_gen

    proc.clean()

    suite = TestSuite([Test(RootGen) for _ in range(tests_in_generation)])

    for generation in range(generations):
        print(f"Generation {generation}")
        suite.run()
        suite.retain_more_valuable(retain_to_next_gen)

        print(proc.get_total_rank())

        for test in suite.tests:
            test.mutate_data()

        suite.tests.extend(
                Test(RootGen) 
                for _ in range(tests_in_generation - retain_to_next_gen)
            ) 

    print(proc.get_coverage())
