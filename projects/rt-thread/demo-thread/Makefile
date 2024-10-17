# make clean && make

PROJ_NAME = rtthread
DEBUG = yes
BENCH = no
FUNC_OPT = yes
MULDIV = no

SRCS = $(wildcard ../libs/*.c) \
       $(wildcard ../libs/*.cpp) \
       $(wildcard ../libs/*.S) \
       $(wildcard user/*.c) \
       $(wildcard rtthread-nano/libcpu/risc-v/*.c) \
       $(wildcard rtthread-nano/libcpu/risc-v/*.S) \
       $(wildcard rtthread-nano/src/*.c)

INC += -I../libs -I./rtthread-nano/include -I./rtthread-nano/libcpu/risc-v -I./user
LDSCRIPT = linker.ld

include ../../../resources/gcc.mk
include ../../../resources/subproject.mk
