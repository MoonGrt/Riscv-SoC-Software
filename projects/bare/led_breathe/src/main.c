#include "cyber.h"

/* 软件延时 */
void delay(unsigned int count)
{
    count *= 10000;
    for (; count != 0; count--)
        ;
}

/* USART initial */
void USART_init(void)
{
    /*GPIO初始化*/
    GPIO_InitTypeDef GPIO_InitStructure;
    GPIO_InitStructure.GPIO_Mode = GPIO_Mode_AF_PP;
    GPIO_InitStructure.GPIO_Pin = GPIO_Pin_0;
    GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
    GPIO_Init(GPIOB, &GPIO_InitStructure); // 将PB0引脚初始化为复用推挽输出
    GPIO_InitStructure.GPIO_Mode = GPIO_Mode_IPU;
    GPIO_InitStructure.GPIO_Pin = GPIO_Pin_1;
    GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
    GPIO_Init(GPIOB, &GPIO_InitStructure); // 将PB1引脚初始化为上拉输入

    /*USART初始化*/
    USART_InitTypeDef USART_InitStructure;                                          // 定义结构体变量
    USART_InitStructure.USART_BaudRate = 115200;                                    // 波特率
    USART_InitStructure.USART_HardwareFlowControl = USART_HardwareFlowControl_None; // 硬件流控制，不需要  可以不配置，默认为None
    USART_InitStructure.USART_Mode = USART_Mode_Tx | USART_Mode_Rx;                 // 模式，发送模式和接收模式均选择
    USART_InitStructure.USART_Parity = USART_Parity_No;                             // 奇偶校验，不需要
    USART_InitStructure.USART_StopBits = USART_StopBits_1;                          // 停止位，选择1位
    USART_InitStructure.USART_WordLength = USART_WordLength_8b;                     // 字长，选择8位
    USART_Init(USART1, &USART_InitStructure);                                       // 将结构体变量交给USART_Init，配置USART1
    /*中断输出配置*/
    USART_ITConfig(USART1, USART_IT_RXNE, ENABLE); // 开启串口接收数据的中断

    // /*NVIC中断分组*/
    // NVIC_PriorityGroupConfig(NVIC_PriorityGroup_2); // 配置NVIC为分组2
    // /*NVIC配置*/
    // NVIC_InitTypeDef NVIC_InitStructure;                      // 定义结构体变量
    // NVIC_InitStructure.NVIC_IRQChannel = USART1_IRQn;         // 选择配置NVIC的USART1线
    // NVIC_InitStructure.NVIC_IRQChannelCmd = ENABLE;           // 指定NVIC线路使能
    // NVIC_InitStructure.NVIC_IRQChannelPreemptionPriority = 1; // 指定NVIC线路的抢占优先级为1
    // NVIC_InitStructure.NVIC_IRQChannelSubPriority = 1;        // 指定NVIC线路的响应优先级为1
    // NVIC_Init(&NVIC_InitStructure);                           // 将结构体变量交给NVIC_Init，配置NVIC外设

    /*USART使能*/
    USART_Cmd(USART1, ENABLE); // 使能USART1，串口开始运行
}

void PWM_init(void)
{
    /*GPIO初始化*/
    GPIO_InitTypeDef GPIO_InitStructure;
    GPIO_InitStructure.GPIO_Mode = GPIO_Mode_AF_PP;
    GPIO_InitStructure.GPIO_Pin = GPIO_Pin_15;
    GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
    GPIO_Init(GPIOA, &GPIO_InitStructure); // 将PA15引脚初始化为复用推挽输出
                                           // 受外设控制的引脚，均需要配置为复用模式

    /*配置时钟源*/
    TIM_InternalClockConfig(TIM2); // 选择TIM3为内部时钟，若不调用此函数，TIM默认也为内部时钟

    /*时基单元初始化*/
    TIM_TimeBaseInitTypeDef TIM_TimeBaseInitStructure;              // 定义结构体变量
    TIM_TimeBaseInitStructure.TIM_ClockDivision = TIM_CKD_DIV1;     // 时钟分频，选择不分频，此参数用于配置滤波器时钟，不影响时基单元功能
    TIM_TimeBaseInitStructure.TIM_CounterMode = TIM_CounterMode_Up; // 计数器模式，选择向上计数
    TIM_TimeBaseInitStructure.TIM_Period = 100 - 1;                 // 计数周期，即ARR的值
    TIM_TimeBaseInitStructure.TIM_Prescaler = 50 - 1;               // 预分频器，即PSC的值
    TIM_TimeBaseInitStructure.TIM_RepetitionCounter = 0;            // 重复计数器，高级定时器才会用到
    TIM_TimeBaseInit(TIM2, &TIM_TimeBaseInitStructure);             // 将结构体变量交给TIM_TimeBaseInit，配置TIM3的时基单元

    /*输出比较初始化*/
    TIM_OCInitTypeDef TIM_OCInitStructure;                        // 定义结构体变量
    TIM_OCStructInit(&TIM_OCInitStructure);                       // 结构体初始化，若结构体没有完整赋值
                                                                  // 则最好执行此函数，给结构体所有成员都赋一个默认值
                                                                  // 避免结构体初值不确定的问题
    TIM_OCInitStructure.TIM_OCMode = TIM_OCMode_PWM1;             // 输出比较模式，选择PWM模式1
    TIM_OCInitStructure.TIM_OCPolarity = TIM_OCPolarity_High;     // 输出极性，选择为高，若选择极性为低，则输出高低电平取反
    TIM_OCInitStructure.TIM_OutputState = TIM_OutputState_Enable; // 输出使能
    TIM_OCInitStructure.TIM_Pulse = 0;                            // 初始的CCR值
    TIM_OC4Init(TIM2, &TIM_OCInitStructure);                      // 将结构体变量交给TIM_OC1Init，配置TIM3的输出比较通道1

    /*TIM使能*/
    TIM_Cmd(TIM2, ENABLE); // 使能TIM3，定时器开始运行
}

uint8_t i; // 定义for循环的变量
void main()
{
    USART_init();
    PWM_init();
    printf("led_breathe\r\n");
    while (1)
    {
        for (i = 0; i <= 100; i++)
        {
            TIM_SetCompare4(TIM2, i); // 依次将定时器的CCR寄存器设置为0~100，PWM占空比逐渐增大，LED逐渐变亮
            delay(5);                 // 延时5ms
        }
        for (i = 0; i <= 100; i++)
        {
            TIM_SetCompare4(TIM2, 100 - i); // 依次将定时器的CCR寄存器设置为100~0，PWM占空比逐渐减小，LED逐渐变暗
            delay(5);                       // 延时5ms
        }
    }
}

void irqCallback()
{
}
