#include "lcd.h"

#define LCD_CLK_PORT    GPIOA
#define LCD_CLK_PIN     GPIO_Pin_4
#define LCD_DATA_PORT   GPIOA
#define LCD_DATA_PIN    GPIO_Pin_5
#define LCD_CS_PORT     GPIOA
#define LCD_CS_PIN      GPIO_Pin_6
#define LCD_RS_PORT     GPIOA
#define LCD_RS_PIN      GPIO_Pin_7
#define LCD_BL_PORT     GPIOA
#define LCD_BL_PIN      GPIO_Pin_8
#define LCD_RST_PORT    GPIOA
#define LCD_RST_PIN     GPIO_Pin_9

#define LCD_CS_H()      GPIO_SetBits(LCD_CS_PORT, LCD_CS_PIN)
#define LCD_CS_L()      GPIO_ResetBits(LCD_CS_PORT, LCD_CS_PIN)
#define LCD_RS_H()      GPIO_SetBits(LCD_RS_PORT, LCD_RS_PIN)
#define LCD_RS_L()      GPIO_ResetBits(LCD_RS_PORT, LCD_RS_PIN)
#define LCD_BL_H()      GPIO_SetBits(LCD_BL_PORT, LCD_BL_PIN)
#define LCD_RST_H()     GPIO_SetBits(LCD_RST_PORT, LCD_RST_PIN)
#define LCD_RST_L()     GPIO_ResetBits(LCD_RST_PORT, LCD_RST_PIN)

void LCD_GPIO_Init(void) {
    GPIO_InitTypeDef GPIO_InitStructure;
    GPIO_InitStructure.GPIO_Pin = LCD_CLK_PIN | LCD_DATA_PIN | LCD_CS_PIN |
                                  LCD_RS_PIN | LCD_BL_PIN | LCD_RST_PIN;
    GPIO_InitStructure.GPIO_Mode = GPIO_Mode_Out_PP;
    GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
    GPIO_Init(GPIOA, &GPIO_InitStructure);
}

void LCD_WriteCmd(uint8_t cmd) {
    LCD_CS_L();
    LCD_RS_L();
    SoftSPI_WriteByte(cmd);
    LCD_CS_H();
}

void LCD_WriteData(uint8_t data) {
    LCD_CS_L();
    LCD_RS_H();
    SoftSPI_WriteByte(data);
    LCD_CS_H();
}

void LCD_Reset(void) {
    LCD_RST_L();
    DelayMs(100);
    LCD_RST_H();
    DelayMs(200);
}

void LCD_Init(void) {
    LCD_Reset();
    LCD_WriteCmd(0x11);
    DelayMs(120);

    const uint16_t init_cmds[] = {
        0x036, 0x170, 0x03A, 0x105, 0x0B2, 0x10C, 0x10C, 0x100, 0x133, 0x133,
        0x0B7, 0x135, 0x0BB, 0x119, 0x0C0, 0x12C, 0x0C2, 0x101, 0x0C3, 0x112,
        0x0C4, 0x120, 0x0C6, 0x10F, 0x0D0, 0x1A4, 0x1A1, 0x0E0, 0x1D0, 0x104,
        0x10D, 0x111, 0x113, 0x12B, 0x13F, 0x154, 0x14C, 0x118, 0x10D, 0x10B,
        0x11F, 0x123, 0x0E1, 0x1D0, 0x104, 0x10C, 0x111, 0x113, 0x12C, 0x13F,
        0x144, 0x151, 0x12F, 0x11F, 0x11F, 0x120, 0x123, 0x021, 0x029,
        0x02A, 0x100, 0x128, 0x101, 0x117,
        0x02B, 0x100, 0x135, 0x100, 0x1BB,
        0x02C
    };

    for (int i = 0; i < sizeof(init_cmds)/sizeof(init_cmds[0]); i++) {
        uint8_t is_data = (init_cmds[i] >> 8) & 0x1;
        uint8_t val = init_cmds[i] & 0xFF;
        if (is_data)
            LCD_WriteData(val);
        else
            LCD_WriteCmd(val);
    }
}

void LCD_Fill_ColorBar(void) {
    for (uint16_t i = 0; i < 32400; i++) {
        uint16_t pixel;
        if (i >= 21600)
            pixel = 0xF800;
        else if (i >= 10800)
            pixel = 0x07E0;
        else
            pixel = 0x001F;

        LCD_WriteData(pixel >> 8);
        LCD_WriteData(pixel & 0xFF);
    }
}

void DelayMs(uint32_t ms) {
    for (uint32_t i = 0; i < ms * 8000; i++) {
        __NOP();
    }
}
