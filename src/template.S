#include "riscv_test.h"

RVTEST_RV32U
RVTEST_CODE_BEGIN

xreg_init:
  la x31, xreg_init_data
  lw x0, 0(x31)
  lw x1, 4(x31)
  lw x2, 8(x31)
  lw x3, 12(x31)
  lw x4, 16(x31)
  lw x5, 20(x31)
  lw x6, 24(x31)
  lw x7, 28(x31)
  lw x8, 32(x31)
  lw x9, 36(x31)
  lw x10, 40(x31)
  lw x11, 44(x31)
  lw x12, 48(x31)
  lw x13, 52(x31)
  lw x14, 56(x31)
  lw x15, 60(x31)
  lw x16, 64(x31)
  lw x17, 68(x31)
  lw x18, 72(x31)
  lw x19, 76(x31)
  lw x20, 80(x31)
  lw x21, 84(x31)
  lw x22, 88(x31)
  lw x23, 92(x31)
  lw x24, 96(x31)
  lw x25, 100(x31)
  lw x26, 104(x31)
  lw x27, 108(x31)
  lw x28, 112(x31)
  lw x29, 116(x31)
  lw x30, 120(x31)
  lw x31, 124(x31)


{text_section}

  RVTEST_PASS

RVTEST_CODE_END

.data

RVTEST_DATA_BEGIN
xreg_init_data:
.word 0x7add33e5
.word 0x94e64d7d
.word 0x00000000
.word 0xffffffff
.word 0x00000000
.word 0xe20990cf
.word 0x00000000
.word 0xa958d1cb
.word 0xffffffff
.word 0x00000000
.word 0x2ffdedfb
.word 0xffffffff
.word 0xffffffff
.word 0x3e8e20bd
.word 0xb23f02f5
.word 0xffffffff
.word 0x746c0ed6
.word 0x00000000
.word 0x6a010a29
.word 0x00000000
.word 0xffffffff
.word 0x621ac237
.word 0xfe902b98
.word 0xffffffff
.word 0xffffffff
.word 0xbce17e1f
.word 0xffffffff
.word 0xffffffff
.word 0xffffffff
.word 0xa969195d
.word 0xffffffff
.word 0xffffffff

{data_section}
RVTEST_DATA_END

