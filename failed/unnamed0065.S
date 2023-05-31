
#include "riscv_macros.h"

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

test_body:  lh x16, test_memory + 16
  
  
  addi x2, x0, 7
  for_3:
  
  addi x23, x0, 21
  for_5:
  
  addi x15, x0, 33
  for_7:
  lh x8, test_memory + 0
  ori x10, x18, -369
  lb x28, test_memory + 24
  addi x15, x15, -1
  bnez x15, for_7
  
  addi x23, x23, -1
  bnez x23, for_5
  
  
  
  addi x24, x0, 37
  for_15:
  ori x1, x10, 1765
  lui x23, 1013770
  
  slt x1, x9, x12
  lui x17, 541164
  sw x25, test_memory + 56, x4
  
  
  addi x23, x0, 32
  for_35:
  
  addi x16, x0, 12
  for_38:
  ori x18, x26, -940
  lbu x11, test_memory + 56
  srai x22, x2, 24
  lui x9, 278098
  addi x16, x16, -1
  bnez x16, for_38
  
  
  
  bltu x11, x18, if_45
  lui x30, 901028
  sw x3, test_memory + 48, x17
  sb x31, test_memory + 48, x9
  auipc x0, 398731
  j endif_45
  if_45:
  sb x22, test_memory + 32, x5
  sh x7, test_memory + 24, x30
  add x5, x12, x8
  sw x2, test_memory + 24, x26
  
  
  blt x27, x7, if_73
  lh x18, test_memory + 48
  lui x26, 60016
  sw x3, test_memory + 32, x15
  sltiu x13, x25, -1413
  j endif_73
  if_73:
  auipc x10, 799437
  lui x11, 883490
  endif_73:
  
  endif_45:
  
  
  
  addi x4, x0, 38
  for_80:
  srl x8, x18, x20
  auipc x15, 740812
  srli x14, x23, 29
  lui x31, 114828
  addi x4, x4, -1
  bnez x4, for_80
  
  
  or x30, x0, x30
  lbu x28, test_memory + 16
  srl x22, x15, x16
  sw x15, test_memory + 24, x16
  addi x23, x23, -1
  bnez x23, for_35
  
  
  srl x22, x12, x27
  addi x24, x24, -1
  bnez x24, for_15
  
  
  lw x1, test_memory + 40
  
  slti x19, x7, 581
  slt x10, x23, x14
  addi x2, x2, -1
  bnez x2, for_3
  

xreg_dump:
  la x31, xreg_dump_data
  sw x0, 0(x31)
  sw x1, 4(x31)
  sw x2, 8(x31)
  sw x3, 12(x31)
  sw x4, 16(x31)
  sw x5, 20(x31)
  sw x6, 24(x31)
  sw x7, 28(x31)
  sw x8, 32(x31)
  sw x9, 36(x31)
  sw x10, 40(x31)
  sw x11, 44(x31)
  sw x12, 48(x31)
  sw x13, 52(x31)
  sw x14, 56(x31)
  sw x15, 60(x31)
  sw x16, 64(x31)
  sw x17, 68(x31)
  sw x18, 72(x31)
  sw x19, 76(x31)
  sw x20, 80(x31)
  sw x21, 84(x31)
  sw x22, 88(x31)
  sw x23, 92(x31)
  sw x24, 96(x31)
  sw x25, 100(x31)
  sw x26, 104(x31)
  sw x27, 108(x31)
  sw x28, 112(x31)
  sw x29, 116(x31)
  sw x30, 120(x31)

RVTEST_PASS

RVTEST_CODE_END

.data
xreg_init_data:
.word 0x170a00fa
.word 0x5b5a7ff4
.word 0x73c5a3d6
.word 0xfc2454e6
.word 0xdf955b2c
.word 0x700526d7
.word 0xbd8948e1
.word 0x34221439
.word 0xd36ef868
.word 0xe1ba5906
.word 0xe41ea7d4
.word 0x35054ec7
.word 0x96c8e65b
.word 0x26fb6ed5
.word 0xd458fb91
.word 0x75c2e010
.word 0x919cc91b
.word 0x84a92da9
.word 0x4d4f71c9
.word 0x5e6afd46
.word 0xbf6f11d8
.word 0xfc35d244
.word 0x28e71bdb
.word 0x1900dcc4
.word 0x68ab9a25
.word 0xd985c7f5
.word 0x9c17f3e0
.word 0x6b680cb5
.word 0xc1036ae0
.word 0xac36495e
.word 0xdd96a3c4
.word 0xdfa3c249

RVTEST_DATA_BEGIN
.align 8
test_memory: .space 64, 0
.align 8
xreg_dump_data: .space 32*4, 0
RVTEST_DATA_END

