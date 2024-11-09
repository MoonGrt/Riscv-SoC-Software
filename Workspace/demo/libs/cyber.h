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



#ifdef CYBER_GPIO
/*!< GPIO */
#include "gpio.h"
#define GPIO_BASE APBPERIPH_BASE + 0x00000
#define GPIOA_BASE (GPIO_BASE + 0x0000)
#define GPIOA ((GPIO_TypeDef *) GPIOA_BASE)
#define GPIOB_BASE (GPIO_BASE + 0x1000)
#define GPIOB ((GPIO_TypeDef *) GPIOB_BASE)
#endif

#ifdef CYBER_USART
/*!< USART */
#include "usart.h"
#define UART_SAMPLE_PER_BAUD 5
#define USART_BASE APBPERIPH_BASE + 0x10000
#define USART1_BASE (USART_BASE + 0x0000)
#define USART1 ((USART_TypeDef *) USART1_BASE)
#define USART2_BASE (USART_BASE + 0x1000)
#define USART2 ((USART_TypeDef *) USART2_BASE)
#endif

#ifdef CYBER_SPI
/*!< SPI */
#include "spi.h"
#define SPI_BASE APBPERIPH_BASE + 0x20000
#define SPI1_BASE (SPI_BASE + 0x0000)
#define SPI1 ((SPI_TypeDef *) SPI1_BASE)
#define SPI2_BASE (SPI_BASE + 0x1000)
#define SPI2 ((SPI_TypeDef *) SPI2_BASE)
#endif

#ifdef CYBER_I2C
/*!< I2C */
#include "i2c.h"
#define I2C_BASE APBPERIPH_BASE + 0x30000
#define I2C1_BASE (I2C_BASE + 0x0000)
#define I2C1 ((I2C_TypeDef *) I2C1_BASE)
#define I2C2_BASE (I2C_BASE + 0x1000)
#define I2C2 ((I2C_TypeDef *) I2C2_BASE)
#endif

#ifdef CYBER_TIM
/*!< TIM */
#include "tim.h"
#define TIM_BASE APBPERIPH_BASE + 0x40000
#define TIM1_BASE (TIM_BASE + 0x0000)
#define TIM1 ((TIM_TypeDef *) TIM1_BASE)
#define TIM2_BASE (TIM_BASE + 0x1000)
#define TIM2 ((TIM_TypeDef *) TIM2_BASE)
#endif

#ifdef CYBER_IWDG
/*!< IWDG */
#include "iwdg.h"
#define IWDG_BASE (0x50000 + 0x0000)
#define IWDG ((IWDG_TypeDef *) IWDG_BASE)
#endif

#ifdef CYBER_WWDG
/*!< WWDG */
#include "wwdg.h"
#define WWDG_BASE (0x50000 + 0x1000)
#define WWDG ((WWDG_TypeDef *) WWDG_BASE)
#endif

#define assert_param(expr) ((void)0)

#endif /* __CYBER_H_ */
