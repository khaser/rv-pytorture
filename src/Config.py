from State import State

class Config:
    iteract_dir = "generated"

    # Control seq command types probability
    mix = {
        'xmem': 25,
        'xalu': 75,
    }

    test_size = 100
    data_size = 2**6

    # Use only seq generator(without branches and function calls) for small blocks
    only_seq_threshold = 5

    max_loop_iterations = 5
    max_loop_nesting = 1

    initial_state = State(0, test_size, max_loop_nesting)

