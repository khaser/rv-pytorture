ENTRYPOINT := src/main.py 
OUTPUT_DIR := generated
TESTPATH := $(OUTPUT_DIR)/test
OPTIONS := $(empty)
CONFIG := default.config
ENV := env/p
CCFLAGS := -nostdlib -nostartfiles -Wa,-march=rv64imafd -I $(ENV) -T $(ENV)/link.ld

SEED = 50 # used for first gentest run, after that it is incremented from each gentest
TEST_COUNT := 100

# NOT USED FOR NIX. TODO: Add shell.nix to repo
# TOOLCHAIN_PREFIX := riscv-64-none 
# CC := $(TOOLCHAIN_PREFIX)-gcc

.phony: gen run clean

define gentest
	[[ -z "$$SEED" ]] && SEED=$(SEED);\
	python3 $(ENTRYPOINT) $(CONFIG) $$SEED > $(TESTPATH).S;\
	$(CC) $(CCFLAGS) $(TESTPATH).S -o $(TESTPATH) &> /dev/null;
endef

gen: $(OUTPUT_DIR)
	$(call gentest)

run: gen
	spike -d $(TESTPATH)

stress: $(OUTPUT_DIR)
	@SEED=$(SEED);\
	for i in $(shell seq 1 $(TEST_COUNT)); do \
		$(call gentest)\
		SEED=$$(($$SEED+1));\
		spike +signature=$(OUTPUT_DIR)/correct.sig $(TESTPATH) || echo Unexpected tohost; \
		spike-broken +signature=$(OUTPUT_DIR)/testing.sig $(TESTPATH); \
		if ( ! diff $(OUTPUT_DIR)/correct.sig $(OUTPUT_DIR)/testing.sig ); then \
			echo test $$i error, seed $$SEED; \
			echo Test stored into $(TESTPATH); \
			break;\
		else \
			echo test $$i passed, seed $$SEED; \
		fi; \
	done

$(OUTPUT_DIR): 
	mkdir $(OUTPUT_DIR)

clean: 
	rm -rf $(OUTPUT_DIR)
