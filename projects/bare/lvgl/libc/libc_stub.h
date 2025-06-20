#ifndef LIBC_STUB_H
#define LIBC_STUB_H

#include <stddef.h>  // for size_t

void *memset(void *s, int c, size_t n);
void *memmove(void *dest, const void *src, size_t n);
size_t strlen(const char *s);
int strcmp(const char *s1, const char *s2);
char *strcpy(char *dest, const char *src);

#endif // LIBC_STUB_H
