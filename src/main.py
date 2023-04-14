#!/usr/bin/env python3.10

import os, sys
import random

from Abstract import AbstractCommandType
from Mem import *
from ALU import *

class Config:
    def __init__(self, lines):
        # TODO: inform about ignored options
        def take_prefix(lines, prefix):
            return (line[len(prefix):] for line in lines if line.startswith(prefix))

        lines = take_prefix(lines, 'torture.generator.')
        self.mix = dict(tuple(line.strip().split()) for line in take_prefix(lines, 'mix.'))

        self.data_size = 2**6 # TODO

class TestWriter:
    def __init__(self, commands, config):
        self.commands = commands
        self.config = config
        
    def __str__(self):
        template_path = os.path.join(__file__, '../template.S')
        template = open(os.path.normpath(template_path), 'r').read()
        return template.format(
                text_section='\n'.join('  ' + str(cmd) for cmd in self.commands),
                data_section=f'.align 8\ntest_memory: .space {config.data_size}, 0'
                )

class Generator:
    def __init__(self, config: Config, seed=None):
        self.config = config

    def next_cmd_block(self, n):
        return [cmd_type.random_command()(self.config) for cmd_type in AbstractCommandType.choices(self.config, n)]

if __name__ == '__main__':
    _, config_filename, seed = sys.argv
    random.seed(seed)

    config = Config(open(sys.argv[1], 'r').readlines())

    gen = Generator(config)
    print(TestWriter(gen.next_cmd_block(5), config))
