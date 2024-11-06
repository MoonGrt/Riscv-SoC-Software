#include "cyber.h"

int main()
{
    // GPIO
    GPIO_InitTypeDef GPIO_InitStructure;
    GPIO_InitStructure.GPIO_Pin = GPIO_Pin_0;
    GPIO_InitStructure.GPIO_Mode = GPIO_Mode_Out_PP;
    GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
    GPIO_Init(GPIOA, &GPIO_InitStructure);
    GPIO_SetBits(GPIOA, GPIO_Pin_0);
    GPIO_ResetBits(GPIOA, GPIO_Pin_0);

    // 创建并配置 DVP 初始化结构体
    DVP_InitTypeDef DVP_InitStructure;
    // 配置 VI 模式
    DVP_InitStructure.VIMode = (VI_CAMERA | EN); // 启用 CAMERA 模式
    // 配置 VP 模式
    DVP_InitStructure.VPMode.Mode = VP_Scaler | EN;          // 启用 Scaler 模式
    DVP_InitStructure.VPMode.CutterMode = VP_Cutter | EN;    // 启用 Cutter 模式
    DVP_InitStructure.VPMode.FilterMode = VP_Gaussian | EN;  // 启用 Gaussian 模式
    DVP_InitStructure.VPMode.ScalerMode = VP_Bilinear | EN;  // 启用 Bilinear 模式
    DVP_InitStructure.VPMode.ColorMode = VP_YUV422 | EN;     // 启用 YUV422 模式
    DVP_InitStructure.VPMode.EdgerMode = VP_Sobel | EN;      // 启用 Sobel 模式
    DVP_InitStructure.VPMode.BinarizerMode = VP_Mirror | EN; // 启用 Mirror 模式
    DVP_InitStructure.VPMode.FillMode = VP_White | EN;       // 启用 白色填充模式
    // 配置 VO 模式
    DVP_InitStructure.VOMode = (VO_HDMI | EN);  // 启用 HDMI 输出模式
    // 初始化 DVP 模块
    DVP_Init(DVP, &DVP_InitStructure);
    // 配置 VP 参数
    DVP_VP_SetStart(DVP, 0, 0);
    DVP_VP_SetEnd(DVP, 1280, 720);
    DVP_VP_SetOutRes(DVP, 1280, 720);
}

void irqCallback()
{
}
