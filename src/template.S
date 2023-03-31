#include "riscv_test.h"

RVTEST_RV64UF
RVTEST_CODE_BEGIN

{text_section}

  j test_pass

  test_fail:
    RVTEST_FAIL
    
  test_pass:
    RVTEST_PASS

RVTEST_CODE_END

.data
RVTEST_DATA_BEGIN
{data_section}
RVTEST_DATA_END

