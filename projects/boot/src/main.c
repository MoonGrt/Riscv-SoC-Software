#include "murax.h"

// 函数声明
void demo_USART(void);
void processCommand(uint8_t command);
void sendResponse(const char *response);

// 主函数
void main()
{
    demo_USART(); // 初始化USART
    while (1)
    {
        // 主循环可以添加其他功能
    }
}

// USART接收数据
uint8_t Serial_RxData; // 串口接收的数据变量
void irqCallback()
{
    if (USART_GetITStatus(USART1, USART_IT_RXNE) == SET) // 判断是否是USART1的接收事件触发的中断
    {
        Serial_RxData = USART_ReceiveData(USART1); // 读取接收数据
        USART_SendData(USART1, Serial_RxData);     // 回显接收到的数据
        processCommand(Serial_RxData);             // 处理接收到的命令
    }
}

// USART初始化
void demo_USART(void)
{
    GPIO_InitTypeDef GPIO_InitStructure;

    // 配置TX引脚（PB0）
    GPIO_InitStructure.GPIO_Pin = GPIO_Pin_0;
    GPIO_InitStructure.GPIO_Mode = GPIO_Mode_AF_PP; // 复用推挽输出
    GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
    GPIO_Init(GPIOB, &GPIO_InitStructure);

    // 配置RX引脚（PB1）
    GPIO_InitStructure.GPIO_Pin = GPIO_Pin_1;
    GPIO_InitStructure.GPIO_Mode = GPIO_Mode_IPU; // 上拉输入
    GPIO_Init(GPIOB, &GPIO_InitStructure);

    // USART初始化
    USART_InitTypeDef USART_InitStructure;
    USART_InitStructure.USART_BaudRate = 115200;                                    // 波特率
    USART_InitStructure.USART_HardwareFlowControl = USART_HardwareFlowControl_None; // 无硬件流控制
    USART_InitStructure.USART_Mode = USART_Mode_Tx | USART_Mode_Rx;                 // 发送和接收模式
    USART_InitStructure.USART_Parity = USART_Parity_No;                             // 无奇偶校验
    USART_InitStructure.USART_StopBits = USART_StopBits_1;                          // 1个停止位
    USART_InitStructure.USART_WordLength = USART_WordLength_8b;                     // 8位数据
    USART_Init(USART1, &USART_InitStructure);                                       // 配置USART1

    USART_ITConfig(USART1, USART_IT_RXNE, ENABLE); // 使能接收中断
    USART_Cmd(USART1, ENABLE);                     // 使能USART1
    sendResponse("UART initialized.\n");
}

// 处理接收到的命令
void processCommand(uint8_t command)
{
    switch (command)
    {
    case 'H': // 如果收到'H'，发送帮助信息
        sendResponse("Help: Send 'H' for help, 'E' to exit.\n");
        break;
    case 'E': // 如果收到'E'，退出或停止功能
        sendResponse("Exiting...\n");
        // 这里可以添加更多退出处理逻辑
        break;
    default:
        sendResponse("Unknown command.\n");
        break;
    }
}

// 发送响应
void sendResponse(const char *response)
{
    while (*response)
    {
        USART_SendData(USART1, *response++); // 逐个发送字符
        while (USART_GetFlagStatus(USART1, USART_FLAG_TXE) == RESET)
            ; // 等待发送完成
    }
}
