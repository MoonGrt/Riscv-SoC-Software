#include "hw_timer.h"
#include "std.h"

#define IRQ_M_TIMER                   7
#define CAUSE_MACHINE_IRQ_REASON_MASK 0xFFFF

uint32_t trap_handler(uint32_t mcause, uint32_t mepc)
{
    uint32_t epc = mepc;
    uint32_t cause = mcause & CAUSE_MACHINE_IRQ_REASON_MASK;

    if (mcause & 0x80000000) 
    {
        /* 异步中断 */
        switch (cause)
        {
            /* 定时器中断 */
            case IRQ_M_TIMER:
                {
                    /* 调用定时器中断处理函数 */
                    hw_timer_irq_handler();
                }
                break;
        }
    }
    else 
    {
        /* 同步中断 */
        /* 目前不需要用到同步中断 */
        printf("Something wrong has happend\n");
    }
    // hw_timer_irq_handler();

    return epc;
}
