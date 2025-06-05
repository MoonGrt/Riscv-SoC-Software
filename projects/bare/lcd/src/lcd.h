#ifndef __LCD_H
#define __LCD_H

#include "cyber.h"
#include "soft_spi.h"

void LCD_GPIO_Init(void);
void LCD_Init(void);
void LCD_Reset(void);
void LCD_WriteCmd(uint8_t cmd);
void LCD_WriteData(uint8_t data);
void LCD_Fill_ColorBar(void);
void DelayMs(uint32_t ms);

#endif