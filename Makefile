PROC_DIR = proc
ENTRYPOINT := src/main.py 
EXE := rv_torture
OUTPUT_DIR := $(PROC_DIR)/sim/tests/$(EXE)
RTL_DIR := $(PROC_DIR)/build/AHB_MAX_imc_IPIC_1_TCM_1_VIRQ_1_TRACE_0
TMP_DIR := generated
ANN_DIR := annotated
RUNINFO_DIR := runinfo

OPTIONS := $(empty)

TOOLCHAIN_PREFIX := riscv64-unknown-elf
CC := $(TOOLCHAIN_PREFIX)-gcc
PROG ?= 
VERBOSE = 0

ifeq ($(VERBOSE), 0)
	OPTIONAL_FD := /dev/null
else
	OPTIONAL_FD := &1
endif

default: run_suite

verilated_model:
	@$(MAKE) -C $(PROC_DIR) build_verilator 2>&1 1>$(OPTIONAL_FD)

define run_single
	echo $(PROG) verilator time: 1>$(OPTIONAL_FD) &&\
	{ cp $(TMP_DIR)/$(PROG).S $(OUTPUT_DIR)/$(EXE).S; time $(MAKE) -C $(PROC_DIR) run_rv_torture_test 2>&1 1>$(OPTIONAL_FD); } 2>$(OPTIONAL_FD) &&\
	{ [ -d $(TMP_DIR)/$(PROG)_runinfo ] && rm -rf $(TMP_DIR)/$(PROG)_runinfo; };\
	mkdir $(TMP_DIR)/$(PROG)_runinfo &&\
	echo $(PROG) spike time: 1>$(OPTIONAL_FD) &&\
	{ time spike -m0x00002000:262144 --pc=0x00002140 --isa=RV32IMC \
	+signature=$(TMP_DIR)/$(PROG)_runinfo/correct.sig --signature-granularity=4 $(RTL_DIR)/$(EXE).elf; } 2>$(OPTIONAL_FD) &&\
	mv $(RTL_DIR)/coverage.dat $(TMP_DIR)/$(PROG)_runinfo &&\
	mv $(RTL_DIR)/$(EXE).sig $(TMP_DIR)/$(PROG)_runinfo/rtl.sig;
endef

run: verilated_model | $(TMP_DIR) $(RUNINFO_DIR)
	@$(call run_single)
	@cp -r $(TMP_DIR)/$(PROG)_runinfo $(RUNINFO_DIR)
	@cd $(RUNINFO_DIR)/$(PROG)_runinfo; diff rtl.sig correct.sig

run_suite: verilated_model | $(TMP_DIR) $(RUNINFO_DIR)
	$(eval PROGS=$(patsubst $(TMP_DIR)/%.S, %, $(wildcard $(TMP_DIR)/*.S)))
	@$(foreach PROG, $(PROGS), $(call run_single))
	verilator_coverage -write $(TMP_DIR)/general_coverage.dat $(TMP_DIR)/*/coverage.dat
	verilator_coverage -rank $(TMP_DIR)/*/coverage.dat > $(TMP_DIR)/general_coverage.rank

get_rank:
	@verilator_coverage -rank $(TMP_DIR)/*/coverage.dat | \
		sed 's/generated\///' | sed 's/_runinfo\/coverage.dat//' | sed 's/[,"]//g' | tail -n +3

get_total_rank:
	@verilator_coverage -rank $(RUNINFO_DIR)/*/coverage.dat | \
		sed 's/generated\///' | sed 's/_runinfo\/coverage.dat//' | sed 's/[,"]//g' | tail -n +3

get_coverage: | $(ANN_DIR)
	@verilator_coverage -annotate $(ANN_DIR) $(RUNINFO_DIR)/*/coverage.dat

$(TMP_DIR):
	mkdir $(TMP_DIR)

$(RUNINFO_DIR):
	mkdir $(RUNINFO_DIR)

$(ANN_DIR):
	mkdir $(ANN_DIR)

rm_tmp:
	@rm -rf $(TMP_DIR)/* 

get_tmp:
	@echo $(TMP_DIR)

rm_results:
	@rm -rf $(RUNINFO_DIR)/*


clean: rm_tmp
	$(MAKE) -C $(PROC_DIR) clean
	@rm -rf $(TMP_DIR) $(RUNINFO_DIR) $(ANN_DIR)

.phony: default clean verilated_model get_rank get_total_rank get_tmp rm_tmp rm_results
