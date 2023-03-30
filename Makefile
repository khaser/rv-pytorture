ENTRYPOINT := src/main.py 
TESTNAME := test
OUTPUT_DIR := generated
OPTIONS := $(empty)
CONFIG := default.config
ENV := env/p
CCFLAGS := -nostdlib -nostartfiles -Wa,-march=rv64imafd -I $(ENV) -T $(ENV)/link.ld

# NOT USED FOR NIX. TODO: Add shell.nix to repo
# TOOLCHAIN_PREFIX := riscv-64-none 
# CC := $(TOOLCHAIN_PREFIX)-gcc

.phony: gen run

gen:
	python3 $(ENTRYPOINT) < $(CONFIG) > $(OUTPUT_DIR)/$(TESTNAME).S
	$(CC) $(CCFLAGS) $(OUTPUT_DIR)/$(TESTNAME).S -o $(OUTPUT_DIR)/$(TESTNAME)

run: gen
	spike -d $(OUTPUT_DIR)/$(TESTNAME)
