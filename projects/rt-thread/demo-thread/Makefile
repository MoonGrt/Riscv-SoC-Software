# make clean && make

PROJ_NAME = rtthread
DEBUG = yes
BENCH = no
FUNC_OPT = yes
MULDIV = no

SRCS = $(wildcard libs/*.c) \
       $(wildcard libs/*.cpp) \
       $(wildcard libs/*.S) \
       $(wildcard user/*.c) \
       $(wildcard rt-thread/libcpu/*.c) \
       $(wildcard rt-thread/libcpu/*.S) \
       $(wildcard rt-thread/src/*.c)

INC += -I./libs -I./rt-thread/include -I./rt-thread/libcpu -I./user
LDSCRIPT = linker.ld

include ../../../resources/gcc.mk
include ../../../resources/subproject.mk
