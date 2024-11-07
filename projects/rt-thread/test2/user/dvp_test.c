/* 头文件声明 */
#include "dvp_test.h"

uint32_t VP_CR = 0x00000000;
uint32_t VP_THRESHOLD = 0x00000000;

int atoi(const char* str) {
    int i = 0;
    int result = 0;
    // 遍历每一个字符
    for (; str[i] != '\0'; i++) {
        if (str[i] < '0' || str[i] > '9')
            return 0; // 如果遇到非数字字符，返回 0（可以按需调整）
        result = result * 10 + (str[i] - '0');  // 将字符转换为数字并累加
    }
    return result;
}

// 复位 DVP
void DVP_Reset(void)
{
    DVP->VP_CR = 0xadbacb;
}
MSH_CMD_EXPORT(DVP_Reset, DVP_Reset)

// 设置 VI
void SetVI(int argc, char** argv)
{
    if (argc != 2)
        printf("SetVI [mode]\r\n");
    else
        DVP->VI_CR = (atoi(argv[1]) & 0x7); // 1位使能 + 2位模式 [2:1]
}
MSH_CMD_EXPORT(SetVI, SetVI)

// 设置 VP
void SetVP(int argc, char** argv)
{
    if (argc != 2)
        printf("SetVP [mode]\r\n");
    else
    {
        VP_CR &= ~(0x07 << 0);
        VP_CR |= ((atoi(argv[1]) & 0x07) << 0);
        DVP->VP_CR = VP_CR;
        printf("%x\r\n", VP_CR);
    }
}
MSH_CMD_EXPORT(SetVP, SetVP)

// 设置 VO
void SetVO(int argc, char** argv)
{
    if (argc != 2)
        printf("SetVO [mode]\r\n");
    else
        DVP->VO_CR = (atoi(argv[1]) & 0x7); // 1位使能 + 2位模式 [2:1]
}
MSH_CMD_EXPORT(SetVO, SetVO)

// 设置 VP 的裁剪模式（Cutter Mode）
void CutterMode(int argc, char** argv) {
    if (argc != 2) {
        printf("Usage: CutterMode [mode]\r\n");
    } else {
        VP_CR &= ~(0x07 << 3);                   // 清除 Cutter 模式位
        VP_CR |= ((atoi(argv[1]) & 0x07) << 3);  // 设置新的 Cutter 模式
        DVP->VP_CR = VP_CR;
        printf("%x\r\n", VP_CR);
    }
}
MSH_CMD_EXPORT(CutterMode, CutterMode);

// 设置 VP 的滤波模式（Filter Mode）
void FilterMode(int argc, char** argv) {
    if (argc != 2) {
        printf("Usage: FilterMode [mode]\r\n");
    } else {
        VP_CR &= ~(0x07 << 6);                   // 清除 Filter 模式位
        VP_CR |= ((atoi(argv[1]) & 0x07) << 6);  // 设置新的 Filter 模式
        DVP->VP_CR = VP_CR;
        printf("%x\r\n", VP_CR);
    }
}
MSH_CMD_EXPORT(FilterMode, FilterMode);

// 设置 VP 的缩放模式（Scaler Mode）
void ScalerMode(int argc, char** argv) {
    if (argc != 2) {
        printf("Usage: ScalerMode [mode]\r\n");
    } else {
        VP_CR &= ~(0x07 << 9);                   // 清除 Scaler 模式位
        VP_CR |= ((atoi(argv[1]) & 0x07) << 9);  // 设置新的 Scaler 模式
        DVP->VP_CR = VP_CR;
        printf("%x\r\n", VP_CR);
    }
}
MSH_CMD_EXPORT(ScalerMode, ScalerMode);

// 设置 VP 的颜色模式（Color Mode）
void ColorMode(int argc, char** argv) {
    if (argc != 2) {
        printf("Usage: ColorMode [mode]\r\n");
    } else {
        VP_CR &= ~(0x07 << 12);                   // 清除 Color 模式位
        VP_CR |= ((atoi(argv[1]) & 0x07) << 12);  // 设置新的 Color 模式
        DVP->VP_CR = VP_CR;
        printf("%x\r\n", VP_CR);
    }
}
MSH_CMD_EXPORT(ColorMode, ColorMode);

// 设置 VP 的边缘检测模式（Edger Mode）
void EdgerMode(int argc, char** argv) {
    if (argc != 2) {
        printf("Usage: EdgerMode [mode]\r\n");
    } else {
        VP_CR &= ~(0x07 << 15);                  // 清除 Edger 模式位
        VP_CR |= ((atoi(argv[1]) & 0x07) << 15); // 设置新的 Edger 模式
        DVP->VP_CR = VP_CR;
        printf("%x\r\n", VP_CR);
    }
}
MSH_CMD_EXPORT(EdgerMode, EdgerMode);

// 设置 VP 的二值化模式（Binarizer Mode）
void BinarizerMode(int argc, char** argv) {
    if (argc != 2) {
        printf("Usage: BinarizerMode [mode]\r\n");
    } else {
        VP_CR &= ~(0x07 << 18);                  // 清除 Binarizer 模式位
        VP_CR |= ((atoi(argv[1]) & 0x07) << 18); // 设置新的 Binarizer 模式
        DVP->VP_CR = VP_CR;
        printf("%x\r\n", VP_CR);
    }
}
MSH_CMD_EXPORT(BinarizerMode, BinarizerMode);

// 设置 VP 的填充模式（Fill Mode）
void FillMode(int argc, char** argv) {
    if (argc != 2) {
        printf("Usage: FillMode [mode]\r\n");
    } else {
        VP_CR &= ~(0x07 << 21);                  // 清除 Fill 模式位
        VP_CR |= ((atoi(argv[1]) & 0x07) << 21); // 设置新的 Fill 模式
        DVP->VP_CR = VP_CR;
        printf("%x\r\n", VP_CR);
    }
}
MSH_CMD_EXPORT(FillMode, FillMode);

// 设置 VP_START
void SetStart(int argc, char** argv)
{
    if (argc != 3)
        printf("SetStart [START_X] [START_Y]\r\n");
    else
        DVP->VP_START = (atoi(argv[2]) & 0xFFFF) << 16 | (atoi(argv[1]) & 0xFFFF); // 将START_Y和START_X写入VP_START
}
MSH_CMD_EXPORT(SetStart, SetStart)

// 设置 VP_END
void SetEnd(int argc, char** argv)
{
    if (argc != 3)
        printf("SetEnd [END_X] [END_Y]\r\n");
    else
        DVP->VP_END = (atoi(argv[2]) & 0xFFFF) << 16 | (atoi(argv[1]) & 0xFFFF); // 将END_Y和END_X写入VP_END
}
MSH_CMD_EXPORT(SetEnd, SetEnd)

// 设置 VP_SCALER
void SetOutRes(int argc, char** argv)
{
    if (argc != 3)
        printf("SetOutRes [OUTPUT_X_RES] [OUTPUT_Y_RES]\r\n");
    else
        DVP->VP_SCALER = (atoi(argv[2]) & 0xFFFF) << 16 | (atoi(argv[1]) & 0xFFFF); // 将OUTPUT_Y_RES和OUTPUT_X_RES写入VP_SCALER
}
MSH_CMD_EXPORT(SetOutRes, SetOutRes)

// 设置 VP_THRESHOLD
void SetThreshold(int argc, char** argv)
{
    if (argc != 3)
        printf("SetThreshold [edge/binarize] [threshold]\r\n");
    else
    {
        if (argv[1][0] == 'e')
        {
            VP_THRESHOLD &= ~(0xFF);
            VP_THRESHOLD |= atoi(argv[2]) & 0xFF;
            DVP->VP_THRESHOLD = VP_THRESHOLD;
            printf("edge %x\r\n", VP_THRESHOLD);
        }
        else
        {
            VP_THRESHOLD &= ~(0xFF << 8);
            VP_THRESHOLD |= (atoi(argv[2]) & 0xFF) << 8;
            DVP->VP_THRESHOLD = VP_THRESHOLD;
            printf("binarize %x\r\n", VP_THRESHOLD);
        }
    }
}
MSH_CMD_EXPORT(SetThreshold, SetThreshold)
