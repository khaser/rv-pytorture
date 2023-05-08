PROC_DIR = proc
ENTRYPOINT := src/main.py 
EXE := rv_torture
OUTPUT_DIR := $(PROC_DIR)/sim/tests/$(EXE)
RTL_DIR := $(PROC_DIR)/build/AHB_MAX_imc_IPIC_1_TCM_1_VIRQ_1_TRACE_0

OPTIONS := $(empty)
CONFIG := default.config

SEED = 78 # used for first gentest run, after that it is incremented from each gentest
TEST_COUNT := 100

TOOLCHAIN_PREFIX := riscv64-unknown-elf
CC := $(TOOLCHAIN_PREFIX)-gcc

default: verilated_model stress

verilated_model:
	$(MAKE) -C $(PROC_DIR) build_verilator

define run
	spike -m0x00002000:262144 --pc=0x00002140 --isa=RV32IMC +signature=$(OUTPUT_DIR)/correct.sig --signature-granularity=4 $(RTL_DIR)/$(EXE).elf || echo Unexpected tohost
endef

run: 
	$(call run)

define gentest
	[[ -z "$$SEED" ]] && SEED=$(SEED);\
	python3 $(ENTRYPOINT) $(CONFIG) $$SEED > $(OUTPUT_DIR)/$(EXE).S
endef

gentest:
	$(call gentest)
	cat $(OUTPUT_DIR)/$(EXE)

stress: | verilated_model
	@SEED=$(SEED); \
	for i in $(shell seq 1 $(TEST_COUNT)); do \
		$(call gentest); \
		SEED=$$(($$SEED+1)); \
		$(MAKE) -C $(PROC_DIR) run_rv_torture_test; \
		$(call run); \
		if ( ! diff $(OUTPUT_DIR)/correct.sig $(RTL_DIR)/$(EXE).sig ); then \
			echo test $$i error, seed $$SEED; \
			break; \
		else \
			echo test $$i passed, seed $$SEED; \
		fi; \
	done

clean: 
	$(MAKE) -C $(PROC_DIR) clean

.phony: default clean stress verilated_model
