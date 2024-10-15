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
    USART_SendData(USART1, 'B');
}

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
    I2C_GenerateSTART(I2C2, ENABLE);                   // 硬件I2C生成起始条件
    I2C_WaitEvent(I2C2, I2C_EVENT_MASTER_MODE_SELECT); // 等待EV5

    I2C_Send7bitAddress(I2C2, DevAddress, I2C_Direction_Transmitter); // 硬件I2C发送从机地址，方向为发送
    I2C_WaitEvent(I2C2, I2C_EVENT_MASTER_TRANSMITTER_MODE_SELECTED);  // 等待EV6

    I2C_SendData(I2C2, RegAddress);                          // 硬件I2C发送寄存器地址
    I2C_WaitEvent(I2C2, I2C_EVENT_MASTER_BYTE_TRANSMITTING); // 等待EV8

    I2C_SendData(I2C2, Data);                               // 硬件I2C发送数据
    I2C_WaitEvent(I2C2, I2C_EVENT_MASTER_BYTE_TRANSMITTED); // 等待EV8_2

    I2C_GenerateSTOP(I2C2, ENABLE); // 硬件I2C生成终止条件
}
/**
 * 函    数：I2C读寄存器
 * 参    数：RegAddress 寄存器地址，范围：参考I2C手册的寄存器描述
 * 返 回 值：读取寄存器的数据，范围：0x00~0xFF
 */
uint8_t I2C_ReadReg(uint8_t DevAddress, uint8_t RegAddress)
{
    uint8_t Data;

    I2C_GenerateSTART(I2C2, ENABLE);                   // 硬件I2C生成起始条件
    I2C_WaitEvent(I2C2, I2C_EVENT_MASTER_MODE_SELECT); // 等待EV5

    I2C_Send7bitAddress(I2C2, DevAddress, I2C_Direction_Transmitter); // 硬件I2C发送从机地址，方向为发送
    I2C_WaitEvent(I2C2, I2C_EVENT_MASTER_TRANSMITTER_MODE_SELECTED);  // 等待EV6

    I2C_SendData(I2C2, RegAddress);                         // 硬件I2C发送寄存器地址
    I2C_WaitEvent(I2C2, I2C_EVENT_MASTER_BYTE_TRANSMITTED); // 等待EV8_2

    I2C_GenerateSTART(I2C2, ENABLE);                   // 硬件I2C生成重复起始条件
    I2C_WaitEvent(I2C2, I2C_EVENT_MASTER_MODE_SELECT); // 等待EV5

    I2C_Send7bitAddress(I2C2, DevAddress, I2C_Direction_Receiver); // 硬件I2C发送从机地址，方向为接收
    I2C_WaitEvent(I2C2, I2C_EVENT_MASTER_RECEIVER_MODE_SELECTED);  // 等待EV6

    I2C_AcknowledgeConfig(I2C2, DISABLE); // 在接收最后一个字节之前提前将应答失能
    I2C_GenerateSTOP(I2C2, ENABLE);       // 在接收最后一个字节之前提前申请停止条件

    I2C_WaitEvent(I2C2, I2C_EVENT_MASTER_BYTE_RECEIVED); // 等待EV7
    Data = I2C_ReceiveData(I2C2);                        // 接收数据寄存器

    I2C_AcknowledgeConfig(I2C2, ENABLE); // 将应答恢复为使能，为了不影响后续可能产生的读取多字节操作

    return Data;
}
void test_I2C(void)
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
    I2C_InitStructure.I2C_OwnAddress1 = 0x00;                                 // 自身地址，从机模式下才有效
    I2C_Init(I2C1, &I2C_InitStructure);                                       // 将结构体变量交给I2C_Init，配置I2C2

    /*I2C使能*/
    I2C_Cmd(I2C1, ENABLE); // 使能I2C1，开始运行
    // /*I2C发送接收*/
    // I2C_WriteReg(0xab, 0xf1, 0x01);
    // I2C_ReadReg(0xab, 0xf2);
}


void test_SPI(void)
{
    /*GPIO初始化*/
    GPIO_InitTypeDef GPIO_InitStructure;
    GPIO_InitStructure.GPIO_Mode = GPIO_Mode_Out_PP;
    GPIO_InitStructure.GPIO_Pin = GPIO_Pin_11;
    GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
    GPIO_Init(GPIOB, &GPIO_InitStructure); // 将PA4引脚初始化为推挽输出

    GPIO_InitStructure.GPIO_Mode = GPIO_Mode_AF_PP;
    GPIO_InitStructure.GPIO_Pin = GPIO_Pin_8 | GPIO_Pin_9;
    GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
    GPIO_Init(GPIOB, &GPIO_InitStructure); // 将PA5和PA7引脚初始化为复用推挽输出

    GPIO_InitStructure.GPIO_Mode = GPIO_Mode_IPU;
    GPIO_InitStructure.GPIO_Pin = GPIO_Pin_10;
    GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
    GPIO_Init(GPIOB, &GPIO_InitStructure); // 将PA6引脚初始化为上拉输入

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
