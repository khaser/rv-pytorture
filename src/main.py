#!/usr/bin/env python3.10
import os, sys
import random
from Mem import *
from ALU import *

# cmd_group_shortcodes = { 'xalu': ALUCommand, 'xmem': MemCommand }
cmd_group_shortcodes = { 'xmem': MemCommand }

class Config:
    def __init__(self, lines):
        # TODO: inform about ignored options

        def take_prefix(lines, prefix):
            return (line.removeprefix(prefix) for line in lines if line.startswith(prefix))

        lines = take_prefix(lines, 'torture.generator.')
        mix_pairs = (tuple(line.strip().split()) for line in take_prefix(lines, 'mix.'))

        self.mix = list((int(w), cmd_group_shortcodes[shortcode]) \
                         for shortcode, w in mix_pairs if cmd_group_shortcodes.get(shortcode) != None)

        self.data_size = 2**12 # TODO

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

# TODO: use special random for each generator
class Generator:
    def __init__(self, config: Config, seed=None):
        self.config = config

    def next_cmd(self):
        weights, cmd_types = zip(*self.config.mix)
        return random.choices(cmd_types, weights)[0]

    def next_cmd_block(self, n):
        weights, cmd_types = zip(*self.config.mix)
        cmds = [cmd_type.random_command()(self.config) for cmd_type in random.choices(cmd_types, weights, k=n)]
        print(cmds, file=sys.stderr)
        return cmds

# TODO: remove random_method static method 

if __name__ == '__main__':
    print(sys.argv, file=sys.stderr)
    _, config_filename, seed = sys.argv
    random.seed(seed)

    config = Config(open(sys.argv[1], 'r').readlines())
    gen = Generator(config)

    # print(gen.next_cmd_block(5), file=sys.stderr)
    print(TestWriter(gen.next_cmd_block(5), config))