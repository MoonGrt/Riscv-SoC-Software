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

.global  trap_entry
trap_entry:
  sw x1,  - 1*4(sp)
  sw x5,  - 2*4(sp)
  sw x6,  - 3*4(sp)
  sw x7,  - 4*4(sp)
  sw x10, - 5*4(sp)
  sw x11, - 6*4(sp)
  sw x12, - 7*4(sp)
  sw x13, - 8*4(sp)
  sw x14, - 9*4(sp)
  sw x15, -10*4(sp)
  sw x16, -11*4(sp)
  sw x17, -12*4(sp)
  sw x28, -13*4(sp)
  sw x29, -14*4(sp)
  sw x30, -15*4(sp)
  sw x31, -16*4(sp)
  addi sp,sp,-16*4
  call irqCallback
  lw x1 , 15*4(sp)
  lw x5,  14*4(sp)
  lw x6,  13*4(sp)
  lw x7,  12*4(sp)
  lw x10, 11*4(sp)
  lw x11, 10*4(sp)
  lw x12,  9*4(sp)
  lw x13,  8*4(sp)
  lw x14,  7*4(sp)
  lw x15,  6*4(sp)
  lw x16,  5*4(sp)
  lw x17,  4*4(sp)
  lw x28,  3*4(sp)
  lw x29,  2*4(sp)
  lw x30,  1*4(sp)
  lw x31,  0*4(sp)
  addi sp,sp,16*4
  mret
  .text

crtInit:
  .option push
  .option norelax
  la gp, __global_pointer$
  .option pop
  la sp, _stack_start

bss_init:
  la a0, _bss_start
  la a1, _bss_end
bss_loop:
  beq a0,a1,bss_done
  sw zero,0(a0)
  add a0,a0,4
  j bss_loop
bss_done:

ctors_init:
  la a0, _ctors_start
  addi sp,sp,-4
ctors_loop:
  la a1, _ctors_end
  beq a0,a1,ctors_done
  lw a3,0(a0)
  add a0,a0,4
  sw a0,0(sp)
  jalr  a3
  lw a0,0(sp)
  j ctors_loop
ctors_done:
  addi sp,sp,4
  li a0, 0x880  // 880 enable timer + external interrupts
  csrw mie,a0
  li a0, 0x1808  // 1808 enable interrupts
  csrw mstatus,a0

  /* 初始化中断 */
  la a0, interrupt_vector_table  # 加载中断向量表地址
  csrw mtvec, a0                 # 设置 mtvec
  li a0, 0x880                   # 开启定时器和外部中断
  csrw mie, a0
  li a0, 0x1808                  # 设置全局中断使能
  csrw mstatus, a0

  /* 跳转到 main */
  call main

infinitLoop:
  j infinitLoop


/* 声明所有中断处理程序为弱符号 */
.weak WDG_IRQHandler
.weak GPIO0_3_IRQHandler
.weak GPIO4_7_IRQHandler
.weak GPIO8_11_IRQHandler
.weak GPIO12_15_IRQHandler
.weak TIM_IRQHandler
.weak USART_IRQHandler
.weak SPI_IRQHandler
.weak I2C_IRQHandler

/* 中断向量表 */
.section .vector, "a", @progbits
  .align 6
  .globl interrupt_vector_table
interrupt_vector_table:
  .word reset_handler      /* 0: 重置中断处理函数 */
  .word wdg_handler        /* 1: 看门狗中断处理函数 */
  .word gpio0_3_handler    /* 2: GPIO 0-3  中断处理函数 */
  .word gpio4_7_handler    /* 3: GPIO 4-7  中断处理函数 */
  .word gpio8_11_handler   /* 4: GPIO 8-11 中断处理函数 */
  .word gpio12_15_handler  /* 5: GPIO 12-15中断处理函数 */
  .word timer_handler      /* 6: 定时器中断处理函数 */
  .word usart_handler      /* 7: USART中断处理函数 */
  .word spi_handler        /* 8: SPI中断处理函数 */
  .word i2c_handler        /* 9: I2C中断处理函数 */

reset_handler:
  j crtStart              /* 重置中断时跳转到程序启动 */
wdg_handler:
  la t0, WDG_IRQHandler     /* 加载目标地址到 t0 */
  jalr t0                   /* 跳转到目标地址 */
gpio0_3_handler:
  la t0, GPIO0_3_IRQHandler
  jalr t0
gpio4_7_handler:
  la t0, GPIO4_7_IRQHandler
  jalr t0
gpio8_11_handler:
  la t0, GPIO8_11_IRQHandler
  jalr t0
gpio12_15_handler:
  la t0, GPIO12_15_IRQHandler
  jalr t0
timer_handler:
  la t0, TIM_IRQHandler
  jalr t0
usart_handler:
  la t0, USART_IRQHandler
  jalr t0
spi_handler:
  la t0, SPI_IRQHandler
  jalr t0
i2c_handler:
  la t0, I2C_IRQHandler
  jalr t0
