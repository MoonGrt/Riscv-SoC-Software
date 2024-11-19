#include "cyber.h"
#include "ov5640.h"

void Camera_Init(void) {
    OV5640_IO_t ov5640_io = {
        .Init       = OV5640_Init,
        .DeInit     = OV5640_DeInit,
        .ReadReg    = ov5640_read_reg,
        .WriteReg   = ov5640_write_reg,
    };
    OV5640_Object_t ov5640;

    if (OV5640_RegisterBusIO(&ov5640, &ov5640_io) != 0) {
        printf("Bus IO registration failed\n");
        return;
    }

    if (OV5640_Init(&ov5640, OV5640_R640x480, OV5640_RGB565) != 0) {
        printf("Camera initialization failed\n");
        return;
    }

    uint32_t camera_id;
    if (OV5640_ReadID(&ov5640, &camera_id) == 0) {
        printf("Camera ID: 0x%08X\n", camera_id);
    }

    OV5640_SetBrightness(&ov5640, 2);
    OV5640_SetContrast(&ov5640, 3);
    OV5640_Start(&ov5640);
}

void main()
{
    Camera_Init();
    while (1) {
        // 主循环
    }
}

void irqCallback()
{
}
