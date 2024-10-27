/* 头文件声明 */
#include "led.h"

/* led 初始化 */
void GPIO_init(void)
{
    GPIO_InitTypeDef GPIO_InitStructure;
    GPIO_InitStructure.GPIO_Pin = GPIO_Pin_0 | GPIO_Pin_1 | GPIO_Pin_2 | GPIO_Pin_3 | GPIO_Pin_4;
    GPIO_InitStructure.GPIO_Mode = GPIO_Mode_Out_PP;
    GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
    GPIO_Init(GPIOA, &GPIO_InitStructure);
}

/* led 线程 入口函数 */
void th_led_en(void *p_arg)
{
    GPIO_init();
    printf("Th_led\r\n");
    for (;;)
    {
        /*使用GPIO_Write，同时设置GPIOA所有引脚的高低电平，实现LED流水灯*/
        GPIO_Write(GPIOA, ~0x0001); // 0000 0000 0000 0001，PA0引脚为低电平，其他引脚均为高电平，注意数据有按位取反
        rt_thread_delay(500);       // 延时10tick
        GPIO_Write(GPIOA, ~0x0002); // 0000 0000 0000 0010，PA1引脚为低电平，其他引脚均为高电平
        rt_thread_delay(500);       // 延时10tick
        GPIO_Write(GPIOA, ~0x0004); // 0000 0000 0000 0100，PA2引脚为低电平，其他引脚均为高电平
        rt_thread_delay(500);       // 延时10tick
        GPIO_Write(GPIOA, ~0x0008); // 0000 0000 0000 1000，PA3引脚为低电平，其他引脚均为高电平
        rt_thread_delay(500);       // 延时10tick
    }
}

/* led 初始化 */
long led_init(void)
{
    /* 初始化线程 */
    rt_thread_init(&th_led,                /* 线程控制块 */
                   "th_led",               /* 线程名称，唯一 */
                   th_led_en,              /* 线程入口地址 */
                   RT_NULL,                /* 线程形参 */
                   &rt_thled_stack[0],     /* 线程栈起始地址 */
                   sizeof(rt_thled_stack), /* 线程栈大小 */
                   6,                      /* 线程优先级 */
                   1);                     /* 线程时间片 */
    /* 启动线程 */
    rt_thread_startup(&th_led);

    printf("led init success\r\n");
}
MSH_CMD_EXPORT(led_init, led init);
