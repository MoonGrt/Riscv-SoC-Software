/* 头文件声明 */
#include <rtthread.h>
#include <rthw.h>
#include <shell.h>
#include "rtconfig.h"
#include "cyber.h"
#include "hw_timer.h"

/* USART 初始化 */
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
    // USART_ITConfig(USART1, USART_IT_RXNE, ENABLE); // 开启串口接收数据的中断

    /*USART使能*/
    USART_Cmd(USART1, ENABLE); // 使能USART1，串口开始运行
}

/* DVP 初始化 */
void DVP_init(void)
{
    // 创建并配置 DVP 初始化结构体
    DVP_InitTypeDef DVP_InitStructure;
    // 配置 VI 模式
    DVP_InitStructure.VIMode = VI_TEST | ENABLE; // 启用 CAMERA 模式
    // 配置 VP 模式
    DVP_InitStructure.VPMode.Mode = VP_Scaler | ENABLE;           // 启用 Scaler 模式
    DVP_InitStructure.VPMode.CutterMode = ENABLE;                 // 启用 Cutter 模式
    DVP_InitStructure.VPMode.FilterMode = ENABLE;                 // 启用 Gaussian 模式
    DVP_InitStructure.VPMode.ScalerMode = VP_Bilinear | ENABLE;   // 启用 Bilinear 模式
    DVP_InitStructure.VPMode.ColorMode = VP_YUV422 | ENABLE;      // 启用 YUV422 模式
    DVP_InitStructure.VPMode.EdgerMode = VP_Sobel | ENABLE;       // 启用 Sobel 模式
    DVP_InitStructure.VPMode.BinarizerMode = VP_Inverse | ENABLE; // 启用 Normal 模式
    DVP_InitStructure.VPMode.FillMode = VP_White | ENABLE;        // 启用 Black填充 模式
    // 配置 VO 模式
    DVP_InitStructure.VOMode = VO_HDMI | ENABLE;  // 启用 HDMI 输出模式
    // 初始化 DVP 模块
    DVP_Init(DVP, &DVP_InitStructure);
    // 配置 VP 参数
    DVP_VP_SetStart(DVP, 0, 0);  // 原图
    DVP_VP_SetEnd(DVP, 1280, 720);
    DVP_VP_SetOutRes(DVP, 1280, 720);
    // 配置 TH
    DVP_VP_SetThreshold(DVP, 0x40, 0x80);
}

/* main 函数 */
int main(void)
{
    /* 硬件初始化 */
    rt_hw_interrupt_disable(); /* 关中断 */
    USART_init();              /* 初始化串口 */
    DVP_init();                /* 初始化DVP */
    hw_timer_init();           /* 初始化硬件定时器 */

    /* 系统定时器列表初始化 */
    rt_system_timer_init();
    /* 调度器初始化 */
    rt_system_scheduler_init();
    /* 初始化 finsh 线程 */
    finsh_system_init();
    /* 启动系统调度器 */
    rt_system_scheduler_start();
}

/* SysTick 中断处理函数 */
void SysTick_Handler(void)
{
    /* 时基更新 */
    rt_tick_increase();
}
