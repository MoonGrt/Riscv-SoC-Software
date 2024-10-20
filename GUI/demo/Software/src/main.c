#include "murax.h"

void demo_GPIO(void);
void demo_WDG(void);
void demo_USART(void);
void demo_I2C(void);
void demo_SPI(void);
void demo_TIM(void);
void demo_PWM(void);

void main()
{
    // demo_GPIO();
    demo_USART();
    // demo_I2C();
    // demo_SPI();
    // demo_TIM();
    // demo_PWM();
    // demo_WDG();

    /*!< old */
    // GPIO
    GPIO_A->OUTPUT_ENABLE = 0x000000FF;
    GPIO_A->OUTPUT = 0x00000001;

    // UART
    Uart_Config uartConfig;
    uartConfig.dataLength = 8;
    uartConfig.parity = NONE;
    uartConfig.stop = ONE;
    uartConfig.clockDivider = CORE_HZ / UART_SAMPLE_PER_BAUD / 115200 - 1;
    uart_applyConfig(UART, &uartConfig);
    // UART->STATUS = 2; // Enable RX interrupts
    UART->DATA = 'A';
    UART->DATA = 'B';

    // TIMER
    // interruptCtrl_init(TIMER_INTERRUPT);
    // prescaler_init(TIMER_PRESCALER);
    // timer_init(TIMER_A);

    // TIMER_PRESCALER->LIMIT = 12000 - 1; // 1 ms rate
    // TIMER_A->LIMIT = 1000 - 1; // 1 second rate
    // TIMER_A->CLEARS_TICKS = 0x00010002;
    // TIMER_INTERRUPT->PENDINGS = 0xF;
    // TIMER_INTERRUPT->MASKS = 0x1;

    // volatile uint32_t a = 1, b = 2, c = 3;
    // uint32_t result = 0;
    // while (1)
    // {
    //     result += a;
    //     result += b + c;
    //     for (uint32_t idx = 0; idx < 50000; idx++)
    //         asm volatile("");
    //     GPIO_A->OUTPUT = (GPIO_A->OUTPUT & ~0x3F) | ((GPIO_A->OUTPUT + 1) & 0x3F); // Counter on LED[5:0]
    // }
}

uint8_t Serial_RxData; // 定义串口接收的数据变量
uint8_t Serial_RxFlag; // 定义串口接收的标志位变量
void irqCallback()
{
#ifdef MURAX_USART
    /*!< USART */
    if (USART_GetITStatus(USART1, USART_IT_RXNE) == SET) // 判断是否是USART1的接收事件触发的中断
    {
        Serial_RxData = USART_ReceiveData(USART1);      // 读取数据寄存器，存放在接收的数据变量
        USART_SendData(USART1, Serial_RxData);
        // Serial_RxData = USART_ReceiveData(USART1);      // 读取数据寄存器，存放在接收的数据变量
        // Serial_RxFlag = 1;                              // 置接收标志位变量为1
        // USART_ClearITPendingBit(USART1, USART_IT_RXNE); // 清除USART1的RXNE标志位
        //                                                 // 读取数据寄存器会自动清除此标志位
        //                                                 // 如果已经读取了数据寄存器，也可以不执行此代码
    }
#endif

#ifdef MURAX_TIM
    /*!< TIM */
    if (TIM_GetITStatus(TIM2, TIM_IT_Update) == SET) // 判断是否是TIM2的更新事件触发的中断
    {
        TIM_ClearITPendingBit(TIM2, TIM_IT_Update); // 清除TIM2更新事件的中断标志位
                                                    // 中断标志位必须清除
                                                    // 否则中断将连续不断地触发，导致主程序卡死
    }
#endif

    /*!< old */
    // if (TIMER_INTERRUPT->PENDINGS & 1)
    // {                           // Timer A interrupt
    //     GPIO_A->OUTPUT ^= 0x80; // Toogle led 7
    //     TIMER_INTERRUPT->PENDINGS = 1;
    // }
    // while (UART->STATUS & (1 << 9))
    // { // UART RX interrupt
    //     UART->DATA = (UART->DATA) & 0xFF;
    // }
}


#ifdef MURAX_GPIO
void demo_GPIO(void)
{
    // RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOA, ENABLE);

    GPIO_InitTypeDef GPIO_InitStructure;
    GPIO_InitStructure.GPIO_Pin = GPIO_Pin_0;
    GPIO_InitStructure.GPIO_Mode = GPIO_Mode_Out_PP;
    GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
    GPIO_Init(GPIOA, &GPIO_InitStructure);
    GPIO_SetBits(GPIOA, GPIO_Pin_0);
    GPIO_ResetBits(GPIOA, GPIO_Pin_0);

    GPIO_InitStructure.GPIO_Pin = GPIO_Pin_1;
    GPIO_InitStructure.GPIO_Mode = GPIO_Mode_Out_OD;
    GPIO_Init(GPIOA, &GPIO_InitStructure);
    GPIO_SetBits(GPIOA, GPIO_Pin_1);
    GPIO_ResetBits(GPIOA, GPIO_Pin_1);
}
#endif

#ifdef MURAX_WDG
void demo_WDG(void)
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
#endif

#ifdef MURAX_USART
void demo_USART(void)
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
    /*USART发送*/
    USART_SendData(USART1, 'A');
    // printf("Murax USART Test\n");
}
#endif

#ifdef MURAX_I2C
/**
 * 函    数：I2C等待事件
 * 参    数：同I2C_CheckEvent
 * 返 回 值：无
 */
void I2C_WaitEvent(I2C_TypeDef *I2Cx, uint32_t I2C_EVENT)
{
    uint32_t Timeout;
    Timeout = 10000;                                   // 给定超时计数时间
    while (I2C_CheckEvent(I2Cx, I2C_EVENT) != SUCCESS) // 循环等待指定事件
    {
        Timeout--;        // 等待时，计数值自减
        if (Timeout == 0) // 自减到0后，等待超时
        {
            /*超时的错误处理代码，可以添加到此处*/
            break; // 跳出等待，不等了
        }
    }
}
/**
 * 函    数：I2C写寄存器
 * 参    数：RegAddress 寄存器地址，范围：参考I2C手册的寄存器描述
 * 参    数：Data 要写入寄存器的数据，范围：0x00~0xFF
 * 返 回 值：无
 */
void I2C_WriteReg(uint8_t DevAddress, uint8_t RegAddress, uint8_t Data)
{
    I2C_GenerateSTART(I2C1, ENABLE);                   // 硬件I2C生成起始条件
    I2C_WaitEvent(I2C1, I2C_EVENT_MASTER_MODE_SELECT); // 等待EV5

    I2C_Send7bitAddress(I2C1, DevAddress, I2C_Direction_Transmitter); // 硬件I2C发送从机地址，方向为发送
    I2C_WaitEvent(I2C1, I2C_EVENT_MASTER_TRANSMITTER_MODE_SELECTED);  // 等待EV6

    I2C_SendData(I2C1, RegAddress);                          // 硬件I2C发送寄存器地址
    I2C_WaitEvent(I2C1, I2C_EVENT_MASTER_BYTE_TRANSMITTING); // 等待EV8

    I2C_SendData(I2C1, Data);                               // 硬件I2C发送数据
    I2C_WaitEvent(I2C1, I2C_EVENT_MASTER_BYTE_TRANSMITTED); // 等待EV8_2

    I2C_GenerateSTOP(I2C1, ENABLE); // 硬件I2C生成终止条件
}
/**
 * 函    数：I2C读寄存器
 * 参    数：RegAddress 寄存器地址，范围：参考I2C手册的寄存器描述
 * 返 回 值：读取寄存器的数据，范围：0x00~0xFF
 */
uint8_t I2C_ReadReg(uint8_t DevAddress, uint8_t RegAddress)
{
    uint8_t Data;

    I2C_GenerateSTART(I2C1, ENABLE);                   // 硬件I2C生成起始条件
    I2C_WaitEvent(I2C1, I2C_EVENT_MASTER_MODE_SELECT); // 等待EV5

    I2C_Send7bitAddress(I2C1, DevAddress, I2C_Direction_Transmitter); // 硬件I2C发送从机地址，方向为发送
    I2C_WaitEvent(I2C1, I2C_EVENT_MASTER_TRANSMITTER_MODE_SELECTED);  // 等待EV6

    I2C_SendData(I2C1, RegAddress);                         // 硬件I2C发送寄存器地址
    I2C_WaitEvent(I2C1, I2C_EVENT_MASTER_BYTE_TRANSMITTED); // 等待EV8_2

    I2C_GenerateSTART(I2C1, ENABLE);                   // 硬件I2C生成重复起始条件
    I2C_WaitEvent(I2C1, I2C_EVENT_MASTER_MODE_SELECT); // 等待EV5

    I2C_Send7bitAddress(I2C1, DevAddress, I2C_Direction_Receiver); // 硬件I2C发送从机地址，方向为接收
    I2C_WaitEvent(I2C1, I2C_EVENT_MASTER_RECEIVER_MODE_SELECTED);  // 等待EV6

    I2C_AcknowledgeConfig(I2C1, DISABLE); // 在接收最后一个字节之前提前将应答失能
    I2C_GenerateSTOP(I2C1, ENABLE);       // 在接收最后一个字节之前提前申请停止条件

    I2C_WaitEvent(I2C1, I2C_EVENT_MASTER_BYTE_RECEIVED); // 等待EV7
    Data = I2C_ReceiveData(I2C1);                        // 接收数据寄存器

    I2C_AcknowledgeConfig(I2C1, ENABLE); // 将应答恢复为使能，为了不影响后续可能产生的读取多字节操作

    return Data;
}
void demo_I2C(void)
{
    /*GPIO初始化*/
    GPIO_InitTypeDef GPIO_InitStructure;
    GPIO_InitStructure.GPIO_Mode = GPIO_Mode_AF_OD;
    GPIO_InitStructure.GPIO_Pin = GPIO_Pin_4 | GPIO_Pin_5;
    GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
    GPIO_Init(GPIOB, &GPIO_InitStructure); // 将PB4和PB5引脚初始化为复用开漏输出

    /*I2C初始化*/
    I2C_InitTypeDef I2C_InitStructure;                                        // 定义结构体变量
    I2C_InitStructure.I2C_Mode = I2C_Mode_I2C;                                // 模式，选择为I2C模式
    I2C_InitStructure.I2C_ClockSpeed = 50000;                                 // 时钟速度，选择为50KHz
    I2C_InitStructure.I2C_DutyCycle = I2C_DutyCycle_2;                        // 时钟占空比，选择Tlow/Thigh = 2
    I2C_InitStructure.I2C_Ack = I2C_Ack_Enable;                               // 应答，选择使能
    I2C_InitStructure.I2C_AcknowledgedAddress = I2C_AcknowledgedAddress_7bit; // 应答地址，选择7位，从机模式下才有效
    I2C_InitStructure.I2C_OwnAddress1 = 0xaa;                                 // 自身地址，从机模式下才有效
    I2C_Init(I2C1, &I2C_InitStructure);                                       // 将结构体变量交给I2C_Init，配置I2C1

    /*I2C使能*/
    I2C_Cmd(I2C1, ENABLE); // 使能I2C1，开始运行
    // /*I2C发送接收*/
    I2C_WriteReg(0xab, 0xf1, 0x01);
    // I2C_ReadReg(0xab, 0xf2);
}
#endif

#ifdef MURAX_SPI
/**
 * 函    数：SPI交换传输一个字节，使用SPI模式0
 * 参    数：ByteSend 要发送的一个字节
 * 返 回 值：接收的一个字节
 */
uint8_t SPI_SwapByte(uint8_t ByteSend)
{
    while (SPI_I2S_GetFlagStatus(SPI1, SPI_I2S_FLAG_TXE) != SET)
        ;                             // 等待发送数据寄存器空
    SPI_I2S_SendData(SPI1, ByteSend); // 写入数据到发送数据寄存器，开始产生时序
    while (SPI_I2S_GetFlagStatus(SPI1, SPI_I2S_FLAG_RXNE) != SET)
        ;                             // 等待接收数据寄存器非空
    return SPI_I2S_ReceiveData(SPI1); // 读取接收到的数据并返回
}
void demo_SPI(void)
{
    /*GPIO初始化*/
    GPIO_InitTypeDef GPIO_InitStructure;
    GPIO_InitStructure.GPIO_Mode = GPIO_Mode_Out_PP;
    GPIO_InitStructure.GPIO_Pin = GPIO_Pin_11;
    GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
    GPIO_Init(GPIOB, &GPIO_InitStructure); // 将PA4引脚初始化为推挽输出 CS
    GPIO_InitStructure.GPIO_Mode = GPIO_Mode_AF_PP;
    GPIO_InitStructure.GPIO_Pin = GPIO_Pin_8 | GPIO_Pin_9;
    GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
    GPIO_Init(GPIOB, &GPIO_InitStructure); // 将PA5和PA7引脚初始化为复用推挽输出 SCK MOSI
    GPIO_InitStructure.GPIO_Mode = GPIO_Mode_IPU;
    GPIO_InitStructure.GPIO_Pin = GPIO_Pin_10;
    GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
    GPIO_Init(GPIOB, &GPIO_InitStructure); // 将PA6引脚初始化为上拉输入 MISO

    /*SPI初始化*/
    SPI_InitTypeDef SPI_InitStructure;                                   // 定义结构体变量
    SPI_InitStructure.SPI_Mode = SPI_Mode_Master;                        // 模式，选择为SPI主模式
    SPI_InitStructure.SPI_Direction = SPI_Direction_2Lines_FullDuplex;   // 方向，选择2线全双工
    SPI_InitStructure.SPI_DataSize = SPI_DataSize_8b;                    // 数据宽度，选择为8位
    SPI_InitStructure.SPI_FirstBit = SPI_FirstBit_MSB;                   // 先行位，选择高位先行
    SPI_InitStructure.SPI_BaudRatePrescaler = SPI_BaudRatePrescaler_128; // 波特率分频，选择128分频
    SPI_InitStructure.SPI_CPOL = SPI_CPOL_Low;                           // SPI极性，选择低极性
    SPI_InitStructure.SPI_CPHA = SPI_CPHA_1Edge;                         // SPI相位，选择第一个时钟边沿采样，极性和相位决定选择SPI模式0
    SPI_InitStructure.SPI_NSS = SPI_NSS_Soft;                            // NSS，选择由软件控制
    SPI_InitStructure.SPI_CRCPolynomial = 7;                             // CRC多项式，暂时用不到，给默认值7
    SPI_Init(SPI1, &SPI_InitStructure);                                  // 将结构体变量交给SPI_Init，配置SPI1

    /*SPI使能*/
    SPI_Cmd(SPI1, ENABLE); // 使能SPI1，开始运行
    /*设置默认电平*/
    GPIO_WriteBit(GPIOA, GPIO_Pin_4, (BitAction)1); // SS默认高电平
    /*SPI交换数据*/
    SPI_SwapByte(0xbb);
}
#endif

#ifdef MURAX_TIM
void demo_TIM(void)
{
    /*配置时钟源*/
    TIM_InternalClockConfig(TIM2); // 选择TIM2为内部时钟，若不调用此函数，TIM默认也为内部时钟

    /*时基单元初始化*/
    TIM_TimeBaseInitTypeDef TIM_TimeBaseInitStructure;              // 定义结构体变量
    TIM_TimeBaseInitStructure.TIM_ClockDivision = TIM_CKD_DIV1;     // 时钟分频，选择不分频，此参数用于配置滤波器时钟，不影响时基单元功能
    TIM_TimeBaseInitStructure.TIM_CounterMode = TIM_CounterMode_Up; // 计数器模式，选择向上计数
    TIM_TimeBaseInitStructure.TIM_Period = 50 - 1;                  // 计数周期，即ARR的值
    TIM_TimeBaseInitStructure.TIM_Prescaler = 72 - 1;               // 预分频器，即PSC的值
    TIM_TimeBaseInitStructure.TIM_RepetitionCounter = 0;            // 重复计数器，高级定时器才会用到
    TIM_TimeBaseInit(TIM2, &TIM_TimeBaseInitStructure);             // 将结构体变量交给TIM_TimeBaseInit，配置TIM2的时基单元

    /*中断输出配置*/
    TIM_ClearFlag(TIM2, TIM_FLAG_Update);      // 清除定时器更新标志位
                                               // TIM_TimeBaseInit函数末尾，手动产生了更新事件
                                               // 若不清除此标志位，则开启中断后，会立刻进入一次中断
                                               // 如果不介意此问题，则不清除此标志位也可
    TIM_ITConfig(TIM2, TIM_IT_Update, ENABLE); // 开启TIM2的更新中断

    // /*NVIC中断分组*/
    // NVIC_PriorityGroupConfig(NVIC_PriorityGroup_2); // 配置NVIC为分组2
    //                                                 // 即抢占优先级范围：0~3，响应优先级范围：0~3
    //                                                 // 此分组配置在整个工程中仅需调用一次
    //                                                 // 若有多个中断，可以把此代码放在main函数内，while循环之前
    //                                                 // 若调用多次配置分组的代码，则后执行的配置会覆盖先执行的配置
    // /*NVIC配置*/
    // NVIC_InitTypeDef NVIC_InitStructure;                      // 定义结构体变量
    // NVIC_InitStructure.NVIC_IRQChannel = TIM2_IRQn;           // 选择配置NVIC的TIM2线
    // NVIC_InitStructure.NVIC_IRQChannelCmd = ENABLE;           // 指定NVIC线路使能
    // NVIC_InitStructure.NVIC_IRQChannelPreemptionPriority = 2; // 指定NVIC线路的抢占优先级为2
    // NVIC_InitStructure.NVIC_IRQChannelSubPriority = 1;        // 指定NVIC线路的响应优先级为1
    // NVIC_Init(&NVIC_InitStructure);                           // 将结构体变量交给NVIC_Init，配置NVIC外设

    /*TIM使能*/
    TIM_Cmd(TIM2, ENABLE); // 使能TIM2，定时器开始运行
}

void demo_PWM(void)
{
    /*GPIO初始化*/
    GPIO_InitTypeDef GPIO_InitStructure;
    GPIO_InitStructure.GPIO_Mode = GPIO_Mode_AF_PP;
    GPIO_InitStructure.GPIO_Pin = GPIO_Pin_12;
    GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
    GPIO_Init(GPIOA, &GPIO_InitStructure); // 将PA8引脚初始化为复用推挽输出
                                           // 受外设控制的引脚，均需要配置为复用模式

    /*配置时钟源*/
    TIM_InternalClockConfig(TIM3); // 选择TIM3为内部时钟，若不调用此函数，TIM默认也为内部时钟

    /*时基单元初始化*/
    TIM_TimeBaseInitTypeDef TIM_TimeBaseInitStructure;              // 定义结构体变量
    TIM_TimeBaseInitStructure.TIM_ClockDivision = TIM_CKD_DIV1;     // 时钟分频，选择不分频，此参数用于配置滤波器时钟，不影响时基单元功能
    TIM_TimeBaseInitStructure.TIM_CounterMode = TIM_CounterMode_Up; // 计数器模式，选择向上计数
    TIM_TimeBaseInitStructure.TIM_Period = 50 - 1;                  // 计数周期，即ARR的值
    TIM_TimeBaseInitStructure.TIM_Prescaler = 72 - 1;               // 预分频器，即PSC的值
    TIM_TimeBaseInitStructure.TIM_RepetitionCounter = 0;            // 重复计数器，高级定时器才会用到
    TIM_TimeBaseInit(TIM3, &TIM_TimeBaseInitStructure);             // 将结构体变量交给TIM_TimeBaseInit，配置TIM3的时基单元

    /*输出比较初始化*/
    TIM_OCInitTypeDef TIM_OCInitStructure;                        // 定义结构体变量
    TIM_OCStructInit(&TIM_OCInitStructure);                       // 结构体初始化，若结构体没有完整赋值
                                                                  // 则最好执行此函数，给结构体所有成员都赋一个默认值
                                                                  // 避免结构体初值不确定的问题
    TIM_OCInitStructure.TIM_OCMode = TIM_OCMode_PWM1;             // 输出比较模式，选择PWM模式1
    TIM_OCInitStructure.TIM_OCPolarity = TIM_OCPolarity_High;     // 输出极性，选择为高，若选择极性为低，则输出高低电平取反
    TIM_OCInitStructure.TIM_OutputState = TIM_OutputState_Enable; // 输出使能
    TIM_OCInitStructure.TIM_Pulse = 0;                            // 初始的CCR值
    TIM_OC1Init(TIM3, &TIM_OCInitStructure);                      // 将结构体变量交给TIM_OC1Init，配置TIM3的输出比较通道1

    /*TIM使能*/
    TIM_Cmd(TIM3, ENABLE); // 使能TIM3，定时器开始运行
    /*PWM输出*/
    TIM_SetCompare1(TIM3, 20);
}
#endif
