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

    GPIO_InitStructure.GPIO_Pin = GPIO_Pin_1;
    GPIO_InitStructure.GPIO_Mode = GPIO_Mode_Out_OD;
    GPIO_Init(GPIOA, &GPIO_InitStructure);
    GPIO_SetBits(GPIOA, GPIO_Pin_1);
    GPIO_ResetBits(GPIOA, GPIO_Pin_1);
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

void test_USART(void)
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

    // /*中断输出配置*/
    // USART_ITConfig(USART1, USART_IT_RXNE, ENABLE); // 开启串口接收数据的中断
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
    USART_SendData(USART1, 'B');
}

void test_IIC(void)
{
    /*GPIO初始化*/
    GPIO_InitTypeDef GPIO_InitStructure;
    GPIO_InitStructure.GPIO_Mode = GPIO_Mode_AF_OD;
    GPIO_InitStructure.GPIO_Pin = GPIO_Pin_10 | GPIO_Pin_11;
    GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
    GPIO_Init(GPIOB, &GPIO_InitStructure); // 将PB10和PB11引脚初始化为复用开漏输出

    /*I2C初始化*/
    I2C_InitTypeDef I2C_InitStructure;                                        // 定义结构体变量
    I2C_InitStructure.I2C_Mode = I2C_Mode_I2C;                                // 模式，选择为I2C模式
    I2C_InitStructure.I2C_ClockSpeed = 50000;                                 // 时钟速度，选择为50KHz
    I2C_InitStructure.I2C_DutyCycle = I2C_DutyCycle_2;                        // 时钟占空比，选择Tlow/Thigh = 2
    I2C_InitStructure.I2C_Ack = I2C_Ack_Enable;                               // 应答，选择使能
    I2C_InitStructure.I2C_AcknowledgedAddress = I2C_AcknowledgedAddress_7bit; // 应答地址，选择7位，从机模式下才有效
    I2C_InitStructure.I2C_OwnAddress1 = 0x00;                                 // 自身地址，从机模式下才有效
    I2C_Init(I2C2, &I2C_InitStructure);                                       // 将结构体变量交给I2C_Init，配置I2C2

    /*I2C使能*/
    I2C_Cmd(I2C2, ENABLE); // 使能I2C2，开始运行
}

void test_SPI(void)
{
    /*GPIO初始化*/
    GPIO_InitTypeDef GPIO_InitStructure;
    GPIO_InitStructure.GPIO_Mode = GPIO_Mode_Out_PP;
    GPIO_InitStructure.GPIO_Pin = GPIO_Pin_4;
    GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
    GPIO_Init(GPIOA, &GPIO_InitStructure); // 将PA4引脚初始化为推挽输出

    GPIO_InitStructure.GPIO_Mode = GPIO_Mode_AF_PP;
    GPIO_InitStructure.GPIO_Pin = GPIO_Pin_5 | GPIO_Pin_7;
    GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
    GPIO_Init(GPIOA, &GPIO_InitStructure); // 将PA5和PA7引脚初始化为复用推挽输出

    GPIO_InitStructure.GPIO_Mode = GPIO_Mode_IPU;
    GPIO_InitStructure.GPIO_Pin = GPIO_Pin_6;
    GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
    GPIO_Init(GPIOA, &GPIO_InitStructure); // 将PA6引脚初始化为上拉输入

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
}

