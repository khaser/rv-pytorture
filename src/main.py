#!/usr/bin/env python3.10

import random, argparse

from Runners import TestSuite, Test
from Generators import RootGen
from Config import Config
import ProcDriver as proc

if __name__ == '__main__':
    parser =  argparse.ArgumentParser('rv-pytorture')
    parser.add_argument('-s', '--seed', type=int)
    parser.add_argument('-g', '--generations', type=int, default=10)
    parser.add_argument('-i', '--tests-in-generation', type=int, default=10)
    parser.add_argument('-r', '--retained-tests-from-generation', type=int, default=1)
    parser.add_argument('-v', '--verbose', action='store_true')

    args = parser.parse_args()

    random.seed(args.seed)

    generations = args.generations
    tests_in_generation = args.tests_in_generation
    retain_to_next_gen = args.retained_tests_from_generation

    Config.verbose = int(args.verbose)

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
