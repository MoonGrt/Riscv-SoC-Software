#ifndef MURAX_H_
#define MURAX_H_

#include "timer.h"
#include "prescaler.h"
#include "interrupt.h"
#include "gpio.h"
#include "uart.h"
#include "conf.h"

#define SRAM_BASE   ((uint32_t)0x00000000)  /*!< SRAM base address */
#define FLASH_BASE  ((uint32_t)0x80000000)  /*!< FLASH base address */
#define PERIPH_BASE ((uint32_t)0xF0000000)  /*!< Peripheral base address */

/*!< Peripheral memory map */
#define APB1PERIPH_BASE PERIPH_BASE
#define APB2PERIPH_BASE (PERIPH_BASE + 0x10000)
#define AHBPERIPH_BASE  (PERIPH_BASE + 0x20000)

// #define GPIOA_BASE (APB1PERIPH_BASE + 0x0800)
// #define GPIOB_BASE (APB1PERIPH_BASE + 0x0C00)
// #define GPIOC_BASE (APB1PERIPH_BASE + 0x1000)
// #define GPIOD_BASE (APB1PERIPH_BASE + 0x1400)
// #define GPIOA ((GPIO_TypeDef *) GPIOA_BASE)
// #define GPIOB ((GPIO_TypeDef *) GPIOB_BASE)
// #define GPIOC ((GPIO_TypeDef *) GPIOC_BASE)
// #define GPIOD ((GPIO_TypeDef *) GPIOD_BASE)
#define GPIOA ((GPIO_TypeDef *)(0xF0030000))
#define GPIOB ((GPIO_TypeDef *)(0xF0031000))
#define GPIOC ((GPIO_TypeDef *)(0xF0032000))
#define GPIOD ((GPIO_TypeDef *)(0xF0033000))






#define CORE_HZ 12000000

#define GPIO_A ((Gpio_Reg *)(0xF0000000))
#define GPIO_B ((Gpio_Reg *)(0xF0000010))
#define GPIO_C ((Gpio_Reg *)(0xF0000020))
#define GPIO_D ((Gpio_Reg *)(0xF0000030))

#define UART ((Uart_Reg *)(0xF0010000))
#define UART_SAMPLE_PER_BAUD 5

#define TIMER_A ((Timer_Reg *)0xF0020040)
#define TIMER_B ((Timer_Reg *)0xF0020050)
#define TIMER_PRESCALER ((Prescaler_Reg *)0xF0020000)
#define TIMER_INTERRUPT ((InterruptCtrl_Reg *)0xF0020010)

#endif /* MURAX_H_ */
