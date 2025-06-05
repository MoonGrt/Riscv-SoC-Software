#include "soft_spi.h"

#define SPI_CLK_H() GPIO_SetBits(GPIOA, GPIO_Pin_4)
#define SPI_CLK_L() GPIO_ResetBits(GPIOA, GPIO_Pin_4)
#define SPI_MOSI_H() GPIO_SetBits(GPIOA, GPIO_Pin_5)
#define SPI_MOSI_L() GPIO_ResetBits(GPIOA, GPIO_Pin_5)

void SoftSPI_WriteByte(uint8_t data) {
    for (int i = 0; i < 8; i++) {
        if (data & 0x80)
            SPI_MOSI_H();
        else
            SPI_MOSI_L();

        SPI_CLK_H();
        for (volatile int j = 0; j < 10; j++);
        SPI_CLK_L();
        for (volatile int j = 0; j < 10; j++);
        data <<= 1;
    }
}
