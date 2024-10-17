# make clean && make

PROJ_NAME = demo
DEBUG = no
BENCH = no
FUNC_OPT = yes
MULDIV = no

SRCS = $(wildcard ../libs/*.c) \
       $(wildcard ../libs/*.cpp) \
       $(wildcard ../libs/*.S) \
       $(wildcard user/*.c) \
       $(wildcard user/*.cpp) \
       $(wildcard user/*.S)

INC += -I ../libs
LDSCRIPT = linker.ld

include ../../../resources/gcc.mk
include ../../../resources/subproject.mk
