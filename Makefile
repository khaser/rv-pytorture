ENTRYPOINT := src/main.py 
OUTPUT_DIR := generated
TESTPATH := $(OUTPUT_DIR)/test
OPTIONS := $(empty)
CONFIG := default.config
ENV := env/p
CCFLAGS := -nostdlib -nostartfiles -Wa,-march=rv64imafd -I $(ENV) -T $(ENV)/link.ld

SEED := 93
TEST_COUNT := 10

# NOT USED FOR NIX. TODO: Add shell.nix to repo
# TOOLCHAIN_PREFIX := riscv-64-none 
# CC := $(TOOLCHAIN_PREFIX)-gcc

.phony: gen run clean

define gentest
	python3 $(ENTRYPOINT) $(CONFIG) $(SEED) > $(TESTPATH).S;\
	$(CC) $(CCFLAGS) $(TESTPATH).S -o $(TESTPATH);
endef

gen: $(OUTPUT_DIR)
	$(call gentest)

run: gen
	spike -d $(TESTPATH)

stress: $(OUTPUT_DIR)
	@for i in $(shell seq 1 $(TEST_COUNT)); do \
		$(call gentest)\
		spike +signature=$(OUTPUT_DIR)/correct.sig $(TESTPATH); \
		spike-broken +signature=$(OUTPUT_DIR)/testing.sig $(TESTPATH); \
		if ( ! diff $(OUTPUT_DIR)/correct.sig $(OUTPUT_DIR)/testing.sig ); then \
			echo test $$i error; \
		else\
			echo test $$i passed; \
		fi; \
	done

$(OUTPUT_DIR): 
	mkdir $(OUTPUT_DIR)

clean: 
	rm -rf $(OUTPUT_DIR)
