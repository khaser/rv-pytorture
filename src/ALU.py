from Abstract import *
import random

class ALUCommand(AbstractCommandType):
    prefix = "xalu"

class ALURtype(ALUCommand):
    def __str__(self):
        return f"{self.cmd} {self.dest}, {self.src1}, {self.src2}"

    def __init__(self, state):
        cmds = ["add", "slt", "sltu", "and", "or", "xor", "sll", "srl", "sub", "sra"]
        if Config.arch.value == 64:
            cmds += ["addw", "subw", "sllw", "srlw", "sraw"]
        self.cmd = random.choice(cmds)
        self.dest, self.src1, self.src2 = state.random_reg(free = True), state.random_reg(), state.random_reg()

class ALUItype(ALUCommand):
    def __str__(self):
        return f"{self.cmd} {self.dest}, {self.src}, {self.immediate}"

    def __init__(self, state):
        short_shifts = []
        shifts = ["slli", "srli", "srai"]
        cmd = ["addi", "slti", "sltiu", "andi", "ori", "xori"]
        cmd_imm = 12
        shift_imm = 5
        if Config.arch.value == 64:
            cmd += ["addiw"]
            short_shifts += ["slliw", "srliw", "sraiw"]
            shift_imm += 1

        self.cmd = random.choice(cmd + shifts + short_shifts)
        self.dest, self.src = state.random_reg(free=True), state.random_reg()

        imm_sz = -1
        if self.cmd in shifts:
            imm_sz = shift_imm
        elif self.cmd in cmd:
            imm_sz = cmd_imm
        else: # self.cmd in short_shifts
            imm_sz = shift_imm - 1

        self.immediate = state.random_imm(imm_sz, neg = self.cmd not in shifts + short_shifts)
