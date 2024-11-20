#ifndef __CYBER_H_
#define __CYBER_H_

typedef enum{RESET = 0, SET = !RESET} FlagStatus, ITStatus;
typedef enum{DISABLE = 0, ENABLE = !DISABLE} FunctionalState;
typedef enum{ERROR = 0, SUCCESS = !ERROR} ErrorStatus;

#include <stdint.h>
#include "config.h"

/*!< Base memory map */
#define SRAM_BASE ((uint32_t)0x80000000)   /*!< SRAM base address */
#define PERIPH_BASE ((uint32_t)0xF0000000) /*!< Peripheral base address */

/*!< Peripheral memory map */
#define APBPERIPH_BASE PERIPH_BASE
#define AHBPERIPH_BASE (PERIPH_BASE + 0x1000000)

/*!< AHB */
#ifdef CYBER_RCC
/*!< RCC */
#include "rcc.h"
#define RCC_BASE (AHBPERIPH_BASE + 0x00000)
#define RCC ((RCC_TypeDef *)RCC_BASE) // 0xF1000000
#endif

#ifdef CYBER_DMA
/*!< DMA */
#include "dma.h"
#define DMA_BASE (AHBPERIPH_BASE + 0x10000)
#define DMA ((DMA_TypeDef *)DMA_BASE) // 0xF1010000
#endif

#ifdef CYBER_DVP
/*!< DVP */
#include "dvp.h"
#define DVP_BASE (AHBPERIPH_BASE + 0x20000)
#define DVP ((DVP_TypeDef *)DVP_BASE) // 0xF1020000
#endif

#ifdef CYBER_GPIO
/*!< GPIO */
#include "gpio.h"
// #define AFIO_BASE (APB2PERIPH_BASE + 0x0000)
// #define AFIO ((AFIO_TypeDef *) AFIO_BASE)
// #define AFIO ((AFIO_TypeDef *)(0xF0030000))
#define GPIOA_BASE (APBPERIPH_BASE + 0x00000)
#define GPIOB_BASE (APBPERIPH_BASE + 0x01000)
#define GPIOA ((GPIO_TypeDef *)GPIOA_BASE) // 0xF0000000
#define GPIOB ((GPIO_TypeDef *)GPIOB_BASE) // 0xF0001000
#endif

#ifdef CYBER_USART
/*!< USART */
#include "usart.h"
#define USART1_BASE (APBPERIPH_BASE + 0x10000)
#define USART2_BASE (APBPERIPH_BASE + 0x11000)
#define USART1 ((USART_TypeDef *)USART1_BASE) // 0xF0010000
#define USART2 ((USART_TypeDef *)USART2_BASE) // 0xF0011000
#endif

#ifdef CYBER_I2C
/*!< I2C */
#include "i2c.h"
#define I2C1_BASE (APBPERIPH_BASE + 0x20000)
#define I2C2_BASE (APBPERIPH_BASE + 0x21000)
#define I2C1 ((I2C_TypeDef *)I2C1_BASE) // 0xF0020000
#define I2C2 ((I2C_TypeDef *)I2C2_BASE) // 0xF0021000
#endif

#ifdef CYBER_SPI
/*!< SPI */
#include "spi.h"
#define SPI1_BASE (APBPERIPH_BASE + 0x30000)
#define SPI2_BASE (APBPERIPH_BASE + 0x31000)
#define SPI1 ((SPI_TypeDef *)SPI1_BASE) // 0xF0030000
#define SPI2 ((SPI_TypeDef *)SPI2_BASE) // 0xF0031000
#endif

#ifdef CYBER_TIM
/*!< TIM */
#include "tim.h"
#define TIM1_BASE (APBPERIPH_BASE + 0x40000)
#define TIM2_BASE (APBPERIPH_BASE + 0x41000)
#define TIM3_BASE (APBPERIPH_BASE + 0x42000)
#define TIM1 ((TIM_TypeDef *)TIM1_BASE) // 0xF0040000
#define TIM1 ((TIM_TypeDef *)TIM2_BASE) // 0xF0041000
#define TIM2 ((TIM_TypeDef *)TIM3_BASE) // 0xF0042000
#endif

#ifdef CYBER_IWDG
/*!< IWDG */
#include "iwdg.h"
#define IWDG_BASE (APBPERIPH_BASE + 0x50000)
#define IWDG ((IWDG_TypeDef *)IWDG_BASE)
#endif

#ifdef CYBER_WWDG
/*!< WWDG */
#include "wwdg.h"
#define WWDG_BASE (APBPERIPH_BASE + 0x51000)
#define WWDG ((WWDG_TypeDef *)WWDG_BASE) // 0xF0051000
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

// #define CORE_HZ 12000000
// #define CORE_HZ 50000000

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

#endif /* __CYBER_H_ */
