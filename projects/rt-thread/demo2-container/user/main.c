/* 头文件声明 */
#include <rtthread.h>
#include "rtconfig.h"
#include "cyber.h"

/* 线程优先级链表 */
extern rt_list_t rt_thread_priority_table[RT_THREAD_PRIORITY_MAX];

/* 线程控制块定义 */
struct rt_thread rt_thread1;
struct rt_thread rt_thread2;

ALIGN(RT_ALIGN_SIZE)
/* 定义线程栈 */
rt_uint8_t rt_thread1_stack[512];
rt_uint8_t rt_thread2_stack[512];

/* 线程声明 */
void thread_1_entry(void *p_arg);
void thread_2_entry(void *p_arg);

/* 函数声明 */
void delay(unsigned int count);

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
    /*Send*/
    USART_SendData(USART1, 'A');
    USART_SendData(USART1, '\n');
}

/* main 函数 */
int main(void)
{
    /* 硬件初始化 */
    USART_init();

    /* 调度器初始化 */
    rt_system_scheduler_init();

    /* 初始化线程 */
    rt_thread_init(&rt_thread1,               /* 线程控制块 */
                   "thread1",                 /* 线程名称，唯一 */
                   thread_1_entry,            /* 线程入口地址 */
                   RT_NULL,                   /* 线程形参 */
                   &rt_thread1_stack[0],      /* 线程栈起始地址 */
                   sizeof(rt_thread1_stack)); /* 线程栈大小 */
    /* 将线程插入就绪列表 */
    rt_list_insert_before(&(rt_thread_priority_table[0]), &(rt_thread1.tlist));

    /* 初始化线程 */
    rt_thread_init(&rt_thread2,               /* 线程控制块 */
                   "thread2",                 /* 线程名称，唯一 */
                   thread_2_entry,            /* 线程入口地址 */
                   RT_NULL,                   /* 线程形参 */
                   &rt_thread2_stack[1],      /* 线程栈起始地址 */
                   sizeof(rt_thread2_stack)); /* 线程栈大小 */
    /* 将线程插入就绪列表 */
    rt_list_insert_before(&(rt_thread_priority_table[1]), &(rt_thread2.tlist));

    /* 启动系统调度器 */
    rt_system_scheduler_start();
}

/* 软件延时 */
void delay(unsigned int count)
{
    count *= 50000;
    for(; count != 0; count--);
}

/* 线程 1 入口函数 */
void thread_1_entry(void *p_arg)
{
    struct rt_object_information *information;

    for ( ;; ) 
    {
        printf("Thread 1 running...\n");
        /* 获取线程对象容器 */
        information = rt_object_get_information(RT_Object_Class_Thread);
        struct rt_object *object = RT_NULL;
        struct rt_list_node *index = RT_NULL;
	    struct rt_list_node *head = &(information->object_list);
        for (index = head->next; index != head; index = index->next)
        {
            object = rt_list_entry(index, struct rt_object, list);
       
            printf("th_name: %s\n", object->name);
            printf("th_type: %d\n", object->type);
            printf("th_flag: %d\n", object->flag);
        }
        delay(100);
        /* 线程切换 */
        rt_schedule();
    }
}

/* 线程 2 入口函数 */
void thread_2_entry(void *p_arg)
{
    for ( ;; ) 
    {
        printf("Thread 2 running...\n");
        delay(100);
        /* 线程切换 */
        rt_schedule();
    }
}
