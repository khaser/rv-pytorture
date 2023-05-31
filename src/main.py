#!/usr/bin/env python3.10

import sys, random, subprocess

from Runners import TestSuite, Test
from Generators import RootGen
from Abstract import parse_rank
from Config import Config

if __name__ == '__main__':
    _, seed = sys.argv
    random.seed(seed)

    generations = 10
    tests_in_generation = 10
    retain_to_next_gen = 3

    subprocess.run("make rm_results -s", shell = True)
    suite = TestSuite([Test(RootGen) for _ in range(tests_in_generation)])

    for generation in range(generations):
        print(f"Generation {generation}")
        suite.run()
        suite.retain_more_valuable(retain_to_next_gen)

        print(sum(map(lambda x : x[2], parse_rank("make get_total_rank"))))

        for test in suite.tests:
            test.mutate_data()

        suite.tests.extend(
                Test(RootGen) 
                for _ in range(tests_in_generation - retain_to_next_gen)
            ) 
