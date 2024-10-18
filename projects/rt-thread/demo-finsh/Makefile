# make clean && make

PROJ_NAME = rtthread
DEBUG = no
BENCH = no
FUNC_OPT = yes
MULDIV = no

SRCS = $(wildcard libs/*.c) \
       $(wildcard libs/*.cpp) \
       $(wildcard libs/*.S) \
       $(wildcard user/*.c) \
       $(wildcard rt-thread/components/finsh/*.c) \
       $(wildcard rt-thread/libcpu/risc-v/*.c) \
       $(wildcard rt-thread/libcpu/risc-v/*.S) \
       $(wildcard rt-thread/src/*.c) \

INC += -I./libs -I./rt-thread/components/finsh -I./rt-thread/include -I./rt-thread/libcpu/risc-v -I./rt-thread/src -I./user
LDSCRIPT = linker.ld

include ../../../resources/gcc.mk
include ../../../resources/subproject.mk
