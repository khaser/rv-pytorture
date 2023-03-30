#!/usr/bin/env python3.10

print("""
#include "riscv_test.h"

RVTEST_RV64UF
RVTEST_CODE_BEGIN

      addi t0, zero, 5
      addi t1, zero, 10
      add t0, t0, t1

      RVTEST_PASS

RVTEST_CODE_END

  .data
RVTEST_DATA_BEGIN

RVTEST_DATA_END
""")
