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
        // printf("Bus IO registration failed\n");
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

int main()
{
    // camera init
    Camera_Init();

    // 创建并配置 DVP 初始化结构体
    DVP_InitTypeDef DVP_InitStructure;
    // 配置 VI 模式
    DVP_InitStructure.VIMode = VI_CAMERA | ENABLE; // 启用 CAMERA 模式
    // 配置 VP 模式
    DVP_InitStructure.VPMode.Mode = VP_Scaler | ENABLE;           // 启用 Scaler 模式
    DVP_InitStructure.VPMode.CutterMode = ENABLE;                 // 启用 Cutter 模式
    DVP_InitStructure.VPMode.FilterMode = VP_Gaussian | ENABLE;   // 启用 Gaussian 模式
    DVP_InitStructure.VPMode.ScalerMode = VP_Bilinear | ENABLE;   // 启用 Bilinear 模式
    DVP_InitStructure.VPMode.ColorMode = VP_YUV422 | ENABLE;      // 启用 YUV422 模式
    DVP_InitStructure.VPMode.EdgerMode = VP_Sobel | ENABLE;       // 启用 Sobel 模式
    DVP_InitStructure.VPMode.BinarizerMode = VP_Inverse | ENABLE; // 启用 Normal 模式
    DVP_InitStructure.VPMode.FillMode = VP_White | ENABLE;        // 启用 Black填充 模式
    // 配置 VO 模式
    DVP_InitStructure.VOMode = VO_HDMI | ENABLE;  // 启用 HDMI 输出模式
    // 初始化 DVP 模块
    DVP_Init(DVP, &DVP_InitStructure);
    // 配置 VP 参数
    // DVP_VP_SetStart(DVP, 0, 0);  // 放大
    // DVP_VP_SetEnd(DVP, 1280 / 2, 720 / 2);
    // DVP_VP_SetOutRes(DVP, 1280, 720);
    DVP_VP_SetStart(DVP, 0, 0);  // 原图
    DVP_VP_SetEnd(DVP, 1280, 720);
    DVP_VP_SetOutRes(DVP, 1280, 720);
    // DVP_VP_SetStart(DVP, 0, 0);  // 缩小
    // DVP_VP_SetEnd(DVP, 1280, 720);
    // DVP_VP_SetOutRes(DVP, 1280 / 2, 720 / 2);
    // 配置 TH
    DVP_VP_SetThreshold(DVP, 0x40, 0x80);
}

void irqCallback()
{
}
