#ifndef __PRESCALER_H_
#define __PRESCALER_H_

typedef struct
{
    volatile uint32_t LIMIT;
} Prescaler_Reg;

static void prescaler_init(Prescaler_Reg *reg)
{
}

#endif /* __PRESCALER_H_ */
