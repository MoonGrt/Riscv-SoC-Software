#ifndef __MURAX_H_
#define __MURAX_H_

typedef enum {RESET = 0, SET = !RESET} FlagStatus, ITStatus;
typedef enum {DISABLE = 0, ENABLE = !DISABLE} FunctionalState;

#include <stdint.h>
#include "gpio.h"
#include "iwdg.h"
#include "wwdg.h"
#include "timer.h"
#include "prescaler.h"
#include "interrupt.h"
#include "usart.h"
#include "conf.h"
#include "vga.h"


/*!< Base memory map */
#define SRAM_BASE   ((uint32_t)0x00000000)  /*!< SRAM base address */
#define FLASH_BASE  ((uint32_t)0x80000000)  /*!< FLASH base address */
#define PERIPH_BASE ((uint32_t)0xF0000000)  /*!< Peripheral base address */

/*!< Peripheral memory map */
#define APB1PERIPH_BASE PERIPH_BASE
#define APB2PERIPH_BASE (PERIPH_BASE + 0x10000)
#define AHBPERIPH_BASE  (PERIPH_BASE + 0x20000)


/*!< GPIO */
// #define GPIOA_BASE (APB1PERIPH_BASE + 0x0800)
// #define GPIOB_BASE (APB1PERIPH_BASE + 0x0C00)
// #define GPIOA ((GPIO_TypeDef *) GPIOA_BASE)
// #define GPIOB ((GPIO_TypeDef *) GPIOB_BASE)
#define GPIOA ((GPIO_TypeDef *)(0xF0030000))
#define GPIOB ((GPIO_TypeDef *)(0xF0031000))

/*!< USART */
// #define USART1_BASE (APB2PERIPH_BASE + 0x3800)
// #define USART1 ((USART_TypeDef *) USART1_BASE)
#define USART1 ((USART_TypeDef *)(0xF0050000))

/*!< WDG */
// #define IWDG_BASE (APB1PERIPH_BASE + 0x3000)
// #define IWDG ((IWDG_TypeDef *) IWDG_BASE)
#define IWDG ((IWDG_TypeDef *)(0xF0040000))
// #define WWDG_BASE (APB1PERIPH_BASE + 0x2C00)
// #define WWDG ((WWDG_TypeDef *) WWDG_BASE)
#define WWDG ((WWDG_TypeDef *)(0xF0041000))





/*!< old */
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

#endif /* __MURAX_H_ */
