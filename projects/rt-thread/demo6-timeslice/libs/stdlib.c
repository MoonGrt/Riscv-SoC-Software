#include <stdarg.h>
#include <stdint.h>
#include "cyber.h"

#ifdef MURAX_USART

extern char *malloc();
extern void putchar(char c);
extern int printf(const char *format, ...);

char heap_memory[1024];
int heap_memory_used = 0;

char *malloc(int size)
{
    char *p = heap_memory + heap_memory_used;
    heap_memory_used += size;
    if (heap_memory_used > 1024)
        asm volatile("ebreak");
    return p;
}

void putchar(char c)
{
    // uart_write(UART, c);
    USART_SendData(USART1, c);
}

static void printf_c(int c)
{
    putchar(c);
}

static void printf_s(char *p)
{
    while (*p)
        putchar(*(p++));
}

static void printf_d(int val)
{
    char buffer[32];
    char *p = buffer;
    if (val < 0)
    {
        printf_c('-');
        val = -val;
    }
    while (val || p == buffer)
    {
        *(p++) = '0' + val % 10;
        val = val / 10;
    }
    while (p != buffer)
        printf_c(*(--p));
}

int printf(const char *format, ...)
{
    int i;
    va_list ap;

    va_start(ap, format);

    for (i = 0; format[i]; i++)
        if (format[i] == '%')
        {
            while (format[++i])
            {
                if (format[i] == 'c')
                {
                    printf_c(va_arg(ap, int));
                    break;
                }
                if (format[i] == 's')
                {
                    printf_s(va_arg(ap, char *));
                    break;
                }
                if (format[i] == 'd')
                {
                    printf_d(va_arg(ap, int));
                    break;
                }
            }
        }
        else
            printf_c(format[i]);

    va_end(ap);
}

int puts(char *s)
{
    while (*s)
    {
        putchar(*s);
        s++;
    }
    putchar('\n');
    return 0;
}

#endif /* MURAX_USART */