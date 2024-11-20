.section .init;
.globl _start;
.type _start, @function

_start:
    j crtInit
    nop
    nop
    nop
    nop
    nop
    nop
    nop

crtInit:
.option push
.option norelax
    la gp, __global_pointer$
.option pop
    la sp, _sp

    /* 将 bss section 初始化为 0 */
bss_init:
    la a0, __bss_start
    la a1, _end
bss_loop:
    beq a0,a1,bss_done
    sw zero,0(a0)
    add a0,a0,4
    j bss_loop
bss_done:

    li a0, 0x880     //880 enable timer + external interrupts
    csrw mie,a0
    li a0, 0x1808     //1808 enable interrupts
    csrw mstatus,a0

    /* 调用初始化函数 */
    call _init
    /* 跳转到 main */
    call main

/* never came here */
loop:
    j loop
