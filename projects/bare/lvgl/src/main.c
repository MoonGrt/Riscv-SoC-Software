#include "cyber.h"
#include "lcd.h"
#include "lvgl.h"
#include "lv_port_disp.h"

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
    /*USART发送*/
    USART_SendData(USART1, 'A');
}

void LCD_Fill_ColorBar(void)
{
    for (uint16_t i = 0; i < 32400; i++) // 135 * 240
    {
        uint16_t pixel;
        if (i >= 21600)
            pixel = 0x001F; // 0xF800
        else if (i >= 10800)
            pixel = 0xF800; // 0x07E0
        else
            pixel = 0x07E0; // 0x001F

        LCD_WriteData(pixel >> 8);
        LCD_WriteData(pixel & 0xFF);
    }
}

void main()
{
    delay_init();
    USART_init();
    LCD_GPIO_Init();     // 初始化 LCD 引脚
    LCD_Init();          // 初始化 LCD 控制器
    // LCD_Fill_ColorBar(); // 显示彩条

    lv_init();            // lv 系统初始化
    lv_port_disp_init();  // lvgl 显示接口初始化，放在lv_init后面
    // lv_port_indev_init(); // lvgl 输入接口初始化，放在 lv_init后面

    // lv_example_btn_1();
    while (1)
    {
        lv_tick_inc(1);
        lv_task_handler();
    }
}

uint8_t Serial_RxData; // 定义串口接收的数据变量
uint8_t Serial_RxFlag; // 定义串口接收的标志位变量
void irqCallback()
{
#ifdef CYBER_USART
    /*!< USART */
    if (USART_GetITStatus(USART1, USART_IT_RXNE) == SET) // 判断是否是USART1的接收事件触发的中断
    {
        Serial_RxData = USART_ReceiveData(USART1); // 读取数据寄存器，存放在接收的数据变量
        USART_SendData(USART1, Serial_RxData);
        // Serial_RxData = USART_ReceiveData(USART1);      // 读取数据寄存器，存放在接收的数据变量
        // Serial_RxFlag = 1;                              // 置接收标志位变量为1
        // USART_ClearITPendingBit(USART1, USART_IT_RXNE); // 清除USART1的RXNE标志位
        //                                                 // 读取数据寄存器会自动清除此标志位
        //                                                 // 如果已经读取了数据寄存器，也可以不执行此代码
    }
#endif

#ifdef CYBER_TIM
    /*!< TIM */
    if (TIM_GetITStatus(TIM1, TIM_IT_Update) == SET) // 判断是否是TIM2的更新事件触发的中断
    {
        TIM_ClearITPendingBit(TIM1, TIM_IT_Update); // 清除TIM2更新事件的中断标志位
                                                    // 中断标志位必须清除
                                                    // 否则中断将连续不断地触发，导致主程序卡死
        USART_SendData(USART1, 'A');                // not "A"
    }
#endif
}
