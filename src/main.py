#!/usr/bin/env python3.10

import sys
import random

from Runners import TestSuite, Test
from Generators import RootGen
from Abstract import Config, State

if __name__ == '__main__':
    _, config_filename, seed = sys.argv
    random.seed(seed)

    config = Config(RootGen, State(0, 50))

    generations = 10
    tests_in_generation = 10
    retain_to_next_gen = 3
    suite = TestSuite([Test(config) for _ in range(tests_in_generation)])

    coverages = []
    
    for generation in range(generations):
        print(f"Generation {generation}")
        suite.run()
        suite.retain_more_valuable(retain_to_next_gen)

        coverages.append(suite.total_coverage)

        for test in suite.tests:
            test.mutate_data()

        suite.tests.extend(
                Test(config) 
                for _ in range(tests_in_generation - retain_to_next_gen)
            ) 

    
    for generation, coverage in enumerate(coverages):
        print(f"Generation: {generation}, coverage: {coverage}")
