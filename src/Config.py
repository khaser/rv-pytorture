import enum

class Arch(enum.Enum):
    RV32I = 32
    RV64I = 64

class Config:
    iteract_dir = "generated"

    arch = Arch.RV32I

    # Control seq command types probability
    mix = {
        'xmem': 50,
        'xalu': 50,
    }

    # Control pattern frequency
    pattern_mix = {
        'seq': 1,
        'branch': 1,
        'loop': 3,
        'func_def': 1, 
        'func_call': 3
    }

    test_size = 100
    data_size = 64

    # Use only seq generator(without branches and function calls) for small blocks
    only_seq_threshold = 5

    max_loop_iterations = 50
    max_loop_nesting = 3
