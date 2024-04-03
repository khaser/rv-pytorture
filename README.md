# RISC-V hardware platform testing tool

### Motivation
The project was created to automatically test the rtl design by generating multiple tests,
running an rtl simulator in parallel, and a demonstration jump.
This idea is also not new in the risc-v ecosystem, for example, the project <https://github.com/ucb-bar/riscv-torture> implements it.
However, it has a number of disadvantages:
it is not able to generate tests with a complex execution flow,
does not take into account past tests and their coverage when generating new ones and so on.

### Dependencies installation
This project uses `nix` to easily create a developer environment.
Nix is the special package manager which can be installed in every linux distribution,
if you have it, you know what to do:
```
nix-shell
```

More usual way is using docker container:
```
docker pull ghcr.io/khaser/rv-pytorture:latest
docker run -it rv-pytorture
```

### Running
```
./src/main.py
```

This command compiles rtl-simulator and runs
Available options can be viewed with `--help` flag.

### Portability
This repository uses `verilator` as a rtl-simulator and `scr1` as
well-documented little riscv core implementation.

Project is designed to be easy portable to other riscv cores and
rtl-simulators. To do this, it's enough to change `Driver.mk` makefile.

### Algorithm and tuning
You can use `Config.py` to setup single test:
preferred test length, control flow complexity,
instruction proportions and so on.

Also, you can setup generative algorithm parameters via
`main.py` options. Algorithm retain some most successful
tests from generation and mutates them before adding to
next generation.
Now, we use verilator coverage info to estimate each test
value. But it can be changed easily in Driver.mk, in case it
doesn't covers the area of interest.

More information you can read in my [thesis on russian](https://drive.google.com/file/d/15URk5rUfiEUEDN2HT2MGECQ6QClPO7WB/view?usp=sharing).
