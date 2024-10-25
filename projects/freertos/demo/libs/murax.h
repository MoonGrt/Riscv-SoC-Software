#ifndef __MURAX_H_
#define __MURAX_H_

typedef enum { RESET = 0, SET = !RESET} FlagStatus, ITStatus;
typedef enum { DISABLE = 0, ENABLE = !DISABLE} FunctionalState;
typedef enum { ERROR = 0, SUCCESS = !ERROR} ErrorStatus;

#include <stdint.h>
#include "config.h"

/*!< Base memory map */
#define SRAM_BASE ((uint32_t)0x00000000)   /*!< SRAM base address */
#define FLASH_BASE ((uint32_t)0x80000000)  /*!< FLASH base address */
#define PERIPH_BASE ((uint32_t)0xF0000000) /*!< Peripheral base address */
#define SRAM_BB_BASE ((uint32_t)0x22000000) /*!< SRAM base address in the bit-band region */
#define PERIPH_BB_BASE ((uint32_t)0x42000000) /*!< Peripheral base address in the bit-band region */

/*!< Peripheral memory map */
#define APB1PERIPH_BASE PERIPH_BASE
#define APB2PERIPH_BASE (PERIPH_BASE + 0x10000)
#define AHBPERIPH_BASE (PERIPH_BASE + 0x20000)

#ifdef MURAX_RCC
/*!< RCC */
#include "rcc.h"
#define RCC_BASE (AHBPERIPH_BASE + 0x1000)
// #define RCC ((RCC_TypeDef *) RCC_BASE)
#define RCC ((RCC_TypeDef *)(0xF0090000))
#endif

#ifdef MURAX_GPIO
/*!< GPIO */
#include "gpio.h"
// #define AFIO_BASE (APB2PERIPH_BASE + 0x0000)
// #define AFIO ((AFIO_TypeDef *) AFIO_BASE)
// #define AFIO ((AFIO_TypeDef *)(0xF0030000))
// #define GPIOA_BASE (APB1PERIPH_BASE + 0x0800)
// #define GPIOB_BASE (APB1PERIPH_BASE + 0x0C00)
// #define GPIOA ((GPIO_TypeDef *) GPIOA_BASE)
// #define GPIOB ((GPIO_TypeDef *) GPIOB_BASE)
#define GPIOA ((GPIO_TypeDef *)(0xF0030000))
#define GPIOB ((GPIO_TypeDef *)(0xF0031000))
#endif

#ifdef MURAX_USART
/*!< USART */
#include "usart.h"
// #define USART1_BASE (APB2PERIPH_BASE + 0x3800)
// #define USART2_BASE (APB1PERIPH_BASE + 0x4400)
// #define USART1 ((USART_TypeDef *) USART1_BASE)
// #define USART2 ((USART_TypeDef *) USART2_BASE)
#define USART1 ((USART_TypeDef *)(0xF0050000))
#define USART2 ((USART_TypeDef *)(0xF0051000))
#endif

#ifdef MURAX_I2C
/*!< I2C */
#include "i2c.h"
// #define I2C1_BASE (APB1PERIPH_BASE + 0x5400)
// #define I2C2_BASE (APB1PERIPH_BASE + 0x5800)
// #define I2C1 ((I2C_TypeDef *) I2C1_BASE)
// #define I2C2 ((I2C_TypeDef *) I2C2_BASE)
#define I2C1 ((I2C_TypeDef *)(0xF0060000))
#define I2C2 ((I2C_TypeDef *)(0xF0061000))
#endif

#ifdef MURAX_SPI
/*!< SPI */
#include "spi.h"
// #define SPI1_BASE (APB2PERIPH_BASE + 0x3000)
// #define SPI2_BASE (APB1PERIPH_BASE + 0x3800)
// #define SPI1 ((SPI_TypeDef *) SPI1_BASE)
// #define SPI2 ((SPI_TypeDef *) SPI2_BASE)
#define SPI1 ((SPI_TypeDef *)(0xF0070000))
#define SPI2 ((SPI_TypeDef *)(0xF0071000))
#endif

#ifdef MURAX_TIM
/*!< TIM */
#include "tim.h"
// #define TIM1_BASE (APB2PERIPH_BASE + 0x2C00)
// #define TIM2_BASE (APB1PERIPH_BASE + 0x0000)
// #define TIM3_BASE (APB1PERIPH_BASE + 0x0400)
// #define TIM1 ((TIM_TypeDef *) TIM1_BASE)
// #define TIM2 ((TIM_TypeDef *) TIM2_BASE)
// #define TIM3 ((TIM_TypeDef *) TIM3_BASE)
// #define TIM1 ((TIM_TypeDef *)(0xF0080000))
#define TIM2 ((TIM_TypeDef *)(0xF0081000))
#define TIM3 ((TIM_TypeDef *)(0xF0082000))
#endif

#ifdef MURAX_WWDG
/*!< WWDG */
#include "wwdg.h"
// #define WWDG_BASE (APB1PERIPH_BASE + 0x2C00)
// #define WWDG ((WWDG_TypeDef *) WWDG_BASE)
#define WWDG ((WWDG_TypeDef *)(0xF0041000))
#endif

#ifdef MURAX_IWDG
/*!< IWDG */
#include "iwdg.h"
// #define IWDG_BASE (APB1PERIPH_BASE + 0x3000)
// #define IWDG ((IWDG_TypeDef *) IWDG_BASE)
#define IWDG ((IWDG_TypeDef *)(0xF0040000))
#endif


/* Exported macro ------------------------------------------------------------*/
#ifdef USE_FULL_ASSERT
/**
 * @brief  The assert_param macro is used for function's parameters check.
 * @param  expr: If expr is false, it calls assert_failed function which reports
 *         the name of the source file and the source line number of the call
 *         that failed. If expr is true, it returns no value.
 * @retval None
 */
#define assert_param(expr) ((expr) ? (void)0 : assert_failed((uint8_t *)__FILE__, __LINE__))
/* Exported functions ------------------------------------------------------- */
void assert_failed(uint8_t *file, uint32_t line); // customization
#else
#define assert_param(expr) ((void)0)
#endif /* USE_FULL_ASSERT */





/*!< old */
#include "timer.h"
#include "interrupt.h"
#include "vga.h"
#include "uart.h"

// #define CORE_HZ 1000000
#define CORE_HZ 50000000

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
