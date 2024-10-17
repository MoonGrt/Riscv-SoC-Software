#include "murax.h"
#include "test.h"

void main()
{
    test_GPIO();
    // test_WDG();
    // test_USART();
    // test_I2C();
    // test_SPI();
    // test_TIM();
    // test_PWM();

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
    /*!< USART */
    // if (USART_GetITStatus(USART1, USART_IT_RXNE) == SET) // 判断是否是USART1的接收事件触发的中断
    // {
    //     Serial_RxData = USART_ReceiveData(USART1);      // 读取数据寄存器，存放在接收的数据变量
    //     USART_SendData(USART1, Serial_RxData);
    //     // Serial_RxData = USART_ReceiveData(USART1);      // 读取数据寄存器，存放在接收的数据变量
    //     // Serial_RxFlag = 1;                              // 置接收标志位变量为1
    //     // USART_ClearITPendingBit(USART1, USART_IT_RXNE); // 清除USART1的RXNE标志位
    //     //                                                 // 读取数据寄存器会自动清除此标志位
    //     //                                                 // 如果已经读取了数据寄存器，也可以不执行此代码
    // }

    // /*!< TIM */
    // if (TIM_GetITStatus(TIM2, TIM_IT_Update) == SET) // 判断是否是TIM2的更新事件触发的中断
    // {
    //     TIM_ClearITPendingBit(TIM2, TIM_IT_Update); // 清除TIM2更新事件的中断标志位
    //                                                 // 中断标志位必须清除
    //                                                 // 否则中断将连续不断地触发，导致主程序卡死
    // }

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
