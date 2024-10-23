.global crtStart
.global main
.global irqCallback

crtStart:
  j crtInit
  nop
  nop
  nop
  nop
  nop
  nop
  nop

//.global  trap_entry
//trap_entry:
//  sw x1,  - 1*4(sp)
//  sw x5,  - 2*4(sp)
//  sw x6,  - 3*4(sp)
//  sw x7,  - 4*4(sp)
//  sw x10, - 5*4(sp)
//  sw x11, - 6*4(sp)
//  sw x12, - 7*4(sp)
//  sw x13, - 8*4(sp)
//  sw x14, - 9*4(sp)
//  sw x15, -10*4(sp)
//  sw x16, -11*4(sp)
//  sw x17, -12*4(sp)
//  sw x28, -13*4(sp)
//  sw x29, -14*4(sp)
//  sw x30, -15*4(sp)
//  sw x31, -16*4(sp)
//  addi sp,sp,-16*4
//  call irqCallback
//  lw x1 , 15*4(sp)
//  lw x5,  14*4(sp)
//  lw x6,  13*4(sp)
//  lw x7,  12*4(sp)
//  lw x10, 11*4(sp)
//  lw x11, 10*4(sp)
//  lw x12,  9*4(sp)
//  lw x13,  8*4(sp)
//  lw x14,  7*4(sp)
//  lw x15,  6*4(sp)
//  lw x16,  5*4(sp)
//  lw x17,  4*4(sp)
//  lw x28,  3*4(sp)
//  lw x29,  2*4(sp)
//  lw x30,  1*4(sp)
//  lw x31,  0*4(sp)
//  addi sp,sp,16*4
//  mret
//  .text







crtInit:
.option push
.option norelax
    la gp, __global_pointer$
.option pop
    la sp, _sp

    /* 把 data section 从 flash 搬运到 ram 中 */
    la a0, _data_lma
    la a1, _data
    la a2, _edata
    bgeu a1, a2, 2f
1:
    lw t0, (a0)      /* 从 flash 中取出一个 word 的数据 */
    sw t0, (a1)      /* 将取出的数据存入 ram 中对应位置 */
    addi a0, a0, 4
    addi a1, a1, 4
    bltu a1, a2, 1b
2:
    /* 将 bss section 初始化为 0 */
    la a0, __bss_start
    la a1, _end
    bgeu a0, a1, 2f
1:
    sw zero, (a0)
    addi a0, a0, 4
    bltu a0, a1, 1b
2:

    /* 调用初始化函数 */
    call _init
    /* 跳转到 main */
    call main

/* never came here */
loop:
    j loop