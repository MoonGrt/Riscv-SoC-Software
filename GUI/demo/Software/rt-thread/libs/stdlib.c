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

static void printf_d(int val, int width)
{
    char buffer[32];
    char *p = buffer;
    int negative = 0;

    if (val < 0)
    {
        negative = 1;
        printf_c('-');
        val = -val;
    }

    while (val || p == buffer)
    {
        *(p++) = '0' + val % 10;
        val = val / 10;
    }

    int len = p - buffer;
    int padding = width - len;
    if (padding > 0)
    {
        for (int i = 0; i < padding; i++)
            printf_c(' ');
    }

    while (p != buffer)
        printf_c(*(--p));
}

static void printf_x(unsigned int val)
{
    char buffer[32];
    char *p = buffer;

    if (val == 0)
    {
        printf_c('0');
        return;
    }

    while (val)
    {
        int digit = val % 16;
        if (digit < 10)
            *(p++) = '0' + digit;
        else
            *(p++) = 'a' + (digit - 10);
        val /= 16;
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
    {
        if (format[i] == '%')
        {
            int width = 0;
            while (format[++i] >= '0' && format[i] <= '9')
            {
                width = width * 10 + (format[i] - '0');
            }

            if (format[i] == 'c')
            {
                printf_c(va_arg(ap, int));
                continue;
            }
            if (format[i] == 's')
            {
                printf_s(va_arg(ap, char *));
                continue;
            }
            if (format[i] == 'd')
            {
                printf_d(va_arg(ap, int), width);
                continue;
            }
            if (format[i] == 'x')
            {
                printf_x(va_arg(ap, unsigned int));
                continue;
            }
        }
        else
        {
            printf_c(format[i]);
        }
    }

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
