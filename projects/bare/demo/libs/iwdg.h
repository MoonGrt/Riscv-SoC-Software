
/* Define to prevent recursive inclusion -------------------------------------*/
#ifndef __IWDG_H
#define __IWDG_H

/* Includes ------------------------------------------------------------------*/
#include "cyber.h"
#ifdef CYBER_IWDG

/** @defgroup IWDG_Exported_Types
 * @{
 */
typedef struct
{
    volatile uint32_t KR;
    volatile uint32_t PR;
    volatile uint32_t RLR;
    volatile uint32_t SR;
} IWDG_TypeDef;

/** @defgroup IWDG_WriteAccess
 * @{
 */
#define IWDG_WriteAccess_Enable ((uint16_t)0x5555)
#define IWDG_WriteAccess_Disable ((uint16_t)0x0000)
#define IS_IWDG_WRITE_ACCESS(ACCESS) (((ACCESS) == IWDG_WriteAccess_Enable) || \
                                      ((ACCESS) == IWDG_WriteAccess_Disable))

/** @defgroup IWDG_prescaler
 * @{
 */
#define IWDG_Prescaler_4 ((uint8_t)0x00)
#define IWDG_Prescaler_8 ((uint8_t)0x01)
#define IWDG_Prescaler_16 ((uint8_t)0x02)
#define IWDG_Prescaler_32 ((uint8_t)0x03)
#define IWDG_Prescaler_64 ((uint8_t)0x04)
#define IWDG_Prescaler_128 ((uint8_t)0x05)
#define IWDG_Prescaler_256 ((uint8_t)0x06)
#define IS_IWDG_PRESCALER(PRESCALER) (((PRESCALER) == IWDG_Prescaler_4) ||   \
                                      ((PRESCALER) == IWDG_Prescaler_8) ||   \
                                      ((PRESCALER) == IWDG_Prescaler_16) ||  \
                                      ((PRESCALER) == IWDG_Prescaler_32) ||  \
                                      ((PRESCALER) == IWDG_Prescaler_64) ||  \
                                      ((PRESCALER) == IWDG_Prescaler_128) || \
                                      ((PRESCALER) == IWDG_Prescaler_256))

/** @defgroup IWDG_Flag
 * @{
 */
#define IWDG_FLAG_PVU ((uint16_t)0x0001)
#define IWDG_FLAG_RVU ((uint16_t)0x0002)
#define IS_IWDG_FLAG(FLAG) (((FLAG) == IWDG_FLAG_PVU) || ((FLAG) == IWDG_FLAG_RVU))
#define IS_IWDG_RELOAD(RELOAD) ((RELOAD) <= 0xFFF)

/** @defgroup IWDG_Exported_Functions
 * @{
 */
void IWDG_WriteAccessCmd(uint16_t IWDG_WriteAccess);
void IWDG_SetPrescaler(uint8_t IWDG_Prescaler);
void IWDG_SetReload(uint16_t Reload);
void IWDG_ReloadCounter(void);
void IWDG_Enable(void);
FlagStatus IWDG_GetFlagStatus(uint16_t IWDG_FLAG);

#endif /* CYBER_IWDG */
#endif /* __IWDG_H */
