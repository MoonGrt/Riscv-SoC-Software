#include <stdarg.h>
#include <stdint.h>
#include "cyber.h"

#ifdef CYBER_USART

void *memset(void *dest, int value, int n);
char *malloc(int size);
int printf(const char *format, ...);

#endif
