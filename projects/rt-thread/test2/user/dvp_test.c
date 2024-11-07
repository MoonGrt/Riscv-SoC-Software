/* 头文件声明 */
#include "dvp_test.h"










static void dvp_test(int argc, char** argv)
{
    rt_uint32_t params;
    if (argc != 2)
        params = "None";
    else
        params = argv[1];

    printf("%s", params);
}
MSH_CMD_EXPORT(dvp_test, dvp test)
