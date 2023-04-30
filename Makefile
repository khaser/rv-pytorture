PROC_DIR = proc
ENTRYPOINT := src/main.py 
OUTPUT_DIR := $(PROC_DIR)/sim/tests/rv_torture
SPIKE_COMPILE_DIR = generated
EXE := rv_torture
SIG := $(PROC_DIR)/build/AHB_MAX_imc_IPIC_1_TCM_1_VIRQ_1_TRACE_0/$(EXE).sig

OPTIONS := $(empty)
CONFIG := default.config
ENV := env/p
CCFLAGS := -nostdlib -nostartfiles -Wa,-march=rv32ima -march=rv32ima -misa-spec=2.2 -mabi=ilp32 -I $(ENV) -T $(ENV)/link.ld

SEED = 50 # used for first gentest run, after that it is incremented from each gentest
TEST_COUNT := 100

TOOLCHAIN_PREFIX := riscv64-unknown-elf
CC := $(TOOLCHAIN_PREFIX)-gcc

default: verilated_model stress

verilated_model:
	$(MAKE) -C $(PROC_DIR) build_verilator

define gentest
	[[ -z "$$SEED" ]] && SEED=$(SEED);\
	python3 $(ENTRYPOINT) $(CONFIG) $$SEED > $(SPIKE_COMPILE_DIR)/$(EXE).S; \
	$(CC) $(CCFLAGS) $(SPIKE_COMPILE_DIR)/$(EXE).S -o $(SPIKE_COMPILE_DIR)/$(EXE);
endef

stress: | $(SPIKE_COMPILE_DIR)
	@SEED=$(SEED); \
	for i in $(shell seq 1 $(TEST_COUNT)); do \
		$(call gentest) \
		SEED=$$(($$SEED+1)); \
		spike --isa=RV32IM +signature=$(SPIKE_COMPILE_DIR)/correct.sig --signature-granularity=4 $(SPIKE_COMPILE_DIR)/$(EXE) || echo Unexpected tohost; \
		sed s/riscv_test/riscv_macros/g $(SPIKE_COMPILE_DIR)/$(EXE).S > $(OUTPUT_DIR)/$(EXE).S; \
		$(MAKE) -C $(PROC_DIR) run_rv_torture_test; \
		tail -n +57 $(SIG) > $(SIG).trim; \
		if ( ! diff $(SPIKE_COMPILE_DIR)/correct.sig $(SIG).trim); then \
			echo test $$i error, seed $$SEED; \
			break; \
		else \
			echo test $$i passed, seed $$SEED; \
		fi; \
	done


$(SPIKE_COMPILE_DIR): 
	mkdir $(SPIKE_COMPILE_DIR)

clean: 
	$(MAKE) -C $(PROC_DIR) clean
	rm -rf generated

.phony: default clean stress verilated_model
