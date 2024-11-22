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
    DVP_init();
}
MSH_CMD_EXPORT(DVP_Reset, DVP_Reset)

// 设置 VI
void VI(int argc, char** argv)
{
    if (argc != 2)
        printf("VI [mode]\r\n");
    else
        DVP->VI_CR = (atoi(argv[1]) & 0x7); // 1位使能 + 2位模式 [2:1]
}
MSH_CMD_EXPORT(VI, VI Mode)

// 设置 VP
void VP(int argc, char** argv)
{
    if (argc != 2)
        printf("VP [mode]\r\n");
    else
    {
        VP_CR &= ~(0x07 << 0);
        VP_CR |= ((atoi(argv[1]) & 0x07) << 0);
        DVP->VP_CR = VP_CR;
        printf("%x\r\n", VP_CR);
    }
}
MSH_CMD_EXPORT(VP, VP Mode)

// 设置 VO
void VO(int argc, char** argv)
{
    if (argc != 2)
        printf("VO [mode]\r\n");
    else
        DVP->VO_CR = (atoi(argv[1]) & 0x7); // 1位使能 + 2位模式 [2:1]
}
MSH_CMD_EXPORT(VO, VO Mode)

// 设置 VP 的裁剪模式（Cutter Mode）
void Cutter(int argc, char** argv) {
    if (argc != 2) {
        printf("Usage: Cutter [mode]\r\n");
    } else {
        VP_CR &= ~(0x07 << 3);                   // 清除 Cutter 模式位
        VP_CR |= ((atoi(argv[1]) & 0x07) << 3);  // 设置新的 Cutter 模式
        DVP->VP_CR = VP_CR;
        printf("%x\r\n", VP_CR);
    }
}
MSH_CMD_EXPORT(Cutter, Cutter Mode);

// 设置 VP 的滤波模式（Filter Mode）
void Filter(int argc, char** argv) {
    if (argc != 2) {
        printf("Usage: Filter [mode]\r\n");
    } else {
        VP_CR &= ~(0x07 << 6);                   // 清除 Filter 模式位
        VP_CR |= ((atoi(argv[1]) & 0x07) << 6);  // 设置新的 Filter 模式
        DVP->VP_CR = VP_CR;
        printf("%x\r\n", VP_CR);
    }
}
MSH_CMD_EXPORT(Filter, Filter Mode);

// 设置 VP 的缩放模式（Scaler Mode）
void Scaler(int argc, char** argv) {
    if (argc != 2) {
        printf("Usage: Scaler [mode]\r\n");
    } else {
        VP_CR &= ~(0x07 << 9);                   // 清除 Scaler 模式位
        VP_CR |= ((atoi(argv[1]) & 0x07) << 9);  // 设置新的 Scaler 模式
        DVP->VP_CR = VP_CR;
        printf("%x\r\n", VP_CR);
    }
}
MSH_CMD_EXPORT(Scaler, Scaler Mode);

// 设置 VP 的颜色模式（Color Mode）
void Color(int argc, char** argv) {
    if (argc != 2) {
        printf("Usage: Color [mode]\r\n");
    } else {
        VP_CR &= ~(0x07 << 12);                   // 清除 Color 模式位
        VP_CR |= ((atoi(argv[1]) & 0x07) << 12);  // 设置新的 Color 模式
        DVP->VP_CR = VP_CR;
        printf("%x\r\n", VP_CR);
    }
}
MSH_CMD_EXPORT(Color, Color Mode);

// 设置 VP 的边缘检测模式（Edger Mode）
void Edger(int argc, char** argv) {
    if (argc != 2) {
        printf("Usage: Edger [mode]\r\n");
    } else {
        VP_CR &= ~(0x07 << 15);                  // 清除 Edger 模式位
        VP_CR |= ((atoi(argv[1]) & 0x07) << 15); // 设置新的 Edger 模式
        DVP->VP_CR = VP_CR;
        printf("%x\r\n", VP_CR);
    }
}
MSH_CMD_EXPORT(Edger, Edger Mode);

// 设置 VP 的二值化模式（Binarizer Mode）
void Binarizer(int argc, char** argv) {
    if (argc != 2) {
        printf("Usage: Binarizer [mode]\r\n");
    } else {
        VP_CR &= ~(0x07 << 18);                  // 清除 Binarizer 模式位
        VP_CR |= ((atoi(argv[1]) & 0x07) << 18); // 设置新的 Binarizer 模式
        DVP->VP_CR = VP_CR;
        printf("%x\r\n", VP_CR);
    }
}
MSH_CMD_EXPORT(Binarizer, Binarizer Mode);

// 设置 VP 的填充模式（Filler Mode）
void Filler(int argc, char** argv) {
    if (argc != 2) {
        printf("Usage: FillMode [mode]\r\n");
    } else {
        VP_CR &= ~(0x07 << 21);                  // 清除 Fill 模式位
        VP_CR |= ((atoi(argv[1]) & 0x07) << 21); // 设置新的 Fill 模式
        DVP->VP_CR = VP_CR;
        printf("%x\r\n", VP_CR);
    }
}
MSH_CMD_EXPORT(Filler, Filler Mode);

// 设置 VP_START
void Start(int argc, char** argv)
{
    if (argc != 3)
        printf("Start [START_X] [START_Y]\r\n");
    else
        DVP->VP_START = (atoi(argv[2]) & 0xFFFF) << 16 | (atoi(argv[1]) & 0xFFFF); // 将START_Y和START_X写入VP_START
}
MSH_CMD_EXPORT(Start, Start)

// 设置 VP_END
void End(int argc, char** argv)
{
    if (argc != 3)
        printf("End [END_X] [END_Y]\r\n");
    else
        DVP->VP_END = (atoi(argv[2]) & 0xFFFF) << 16 | (atoi(argv[1]) & 0xFFFF); // 将END_Y和END_X写入VP_END
}
MSH_CMD_EXPORT(End, End)

// 设置 VP_SCALER
void OutRes(int argc, char** argv)
{
    if (argc != 3)
        printf("OutRes [OUTPUT_X_RES] [OUTPUT_Y_RES]\r\n");
    else
        DVP->VP_SCALER = (atoi(argv[2]) & 0xFFFF) << 16 | (atoi(argv[1]) & 0xFFFF); // 将OUTPUT_Y_RES和OUTPUT_X_RES写入VP_SCALER
}
MSH_CMD_EXPORT(OutRes, OutRes)

// 设置 VP_THRESHOLD
void Threshold(int argc, char** argv)
{
    if (argc != 3)
        printf("Threshold [edge/binarize] [threshold]\r\n");
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
MSH_CMD_EXPORT(Threshold, Threshold)
