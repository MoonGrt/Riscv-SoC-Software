#include "test.h"
#include "murax.h"

void test_GPIO(void)
{
    GPIO_InitTypeDef GPIO_InitStructure;
    GPIO_InitStructure.GPIO_Pin = GPIO_Pin_0;
    GPIO_InitStructure.GPIO_Mode = GPIO_Mode_Out_PP;
    GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
    GPIO_Init(GPIOA, &GPIO_InitStructure);
    GPIO_SetBits(GPIOA, GPIO_Pin_0);
    GPIO_ResetBits(GPIOA, GPIO_Pin_0);
    GPIO_Init(GPIOB, &GPIO_InitStructure);
    GPIO_SetBits(GPIOB, GPIO_Pin_0);
    GPIO_ResetBits(GPIOB, GPIO_Pin_0);

    GPIO_InitStructure.GPIO_Pin = GPIO_Pin_1;
    GPIO_InitStructure.GPIO_Mode = GPIO_Mode_Out_OD;
    GPIO_Init(GPIOA, &GPIO_InitStructure);
    GPIO_SetBits(GPIOA, GPIO_Pin_1);
    GPIO_ResetBits(GPIOA, GPIO_Pin_1);
    GPIO_Init(GPIOB, &GPIO_InitStructure);
    GPIO_SetBits(GPIOB, GPIO_Pin_1);
    GPIO_ResetBits(GPIOB, GPIO_Pin_1);

    // GPIO_InitStructure.GPIO_Pin = GPIO_Pin_2;
    // GPIO_InitStructure.GPIO_Mode = GPIO_Mode_AF_OD;
    // GPIO_Init(GPIOA, &GPIO_InitStructure);

    // GPIO_InitStructure.GPIO_Pin = GPIO_Pin_3;
    // GPIO_InitStructure.GPIO_Mode = GPIO_Mode_AF_PP;
    // GPIO_Init(GPIOA, &GPIO_InitStructure);
}

void test_WDG(void)
{
    /*IWDG初始化*/
    IWDG_WriteAccessCmd(IWDG_WriteAccess_Enable); // 独立看门狗写使能
    IWDG_SetPrescaler(IWDG_Prescaler_16);         // 设置预分频为16
    IWDG_SetReload(100);                          // 设置重装值为2499，独立看门狗的超时时间为1000ms
    IWDG_ReloadCounter();                         // 重装计数器，喂狗
    IWDG_Enable();                                // 独立看门狗使能
    /*IWDG喂狗*/
    IWDG_ReloadCounter(); // 重装计数器，喂狗

    /*WWDG初始化*/
    WWDG_SetPrescaler(WWDG_Prescaler_8); // 设置预分频为8
    WWDG_SetWindowValue(0x40 | 21);      // 设置窗口值21，窗口时间为30ms  // 如果喂狗太早, 复位
    WWDG_Enable(0x40 | 54);              // 使能并第一次喂狗，超时时间为50ms
    /*WWDG喂狗*/
    WWDG_SetCounter(0x40 | 54); // 重装计数器，喂狗
}
