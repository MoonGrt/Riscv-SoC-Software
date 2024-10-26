# make clean && make

PROJ_NAME = blinky
DEBUG = yes
BENCH = no
FUNC_OPT = yes
MULDIV = yes

SRCS = $(wildcard libs/*.c) \
       $(wildcard user/*.c) \
       $(wildcard user/*.S) \
       $(wildcard freertos/src/*.c) \
       $(wildcard freertos/src/*.S) \
       $(wildcard freertos/portable/RISC-V/*.c) \
       $(wildcard freertos/portable/RISC-V/*.S) \
       $(wildcard freertos/portable/MemMang/heap_1.c) \

INC += -I./libs -I./user -I./freertos/include -I./freertos/portable/RISC-V
LDSCRIPT = link.lds

include ../gcc.mk
include ../subproject.mk
