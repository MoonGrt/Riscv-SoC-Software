#ifndef __INTERRUPT_H_
#define __INTERRUPT_H_

typedef struct
{
    volatile uint32_t PENDINGS;
    volatile uint32_t MASKS;
} InterruptCtrl_Reg;

static void interruptCtrl_init(InterruptCtrl_Reg *reg)
{
    reg->MASKS = 0;
    reg->PENDINGS = 0xFFFFFFFF;
}

#endif /* __INTERRUPT_H_ */