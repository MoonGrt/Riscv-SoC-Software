# make clean && make

PROJ_NAME = container
DEBUG = yes
BENCH = no
FUNC_OPT = yes
MULDIV = yes

SRCS = $(wildcard libs/*.c) \
       $(wildcard user/*.c) \
       $(wildcard user/*.S) \
       $(wildcard rt-thread/libcpu/*.c) \
       $(wildcard rt-thread/libcpu/*.S) \
       $(wildcard rt-thread/src/*.c)

INC += -I./libs -I./rt-thread/include -I./rt-thread/libcpu -I./user
LDSCRIPT = link.lds

include ../gcc.mk
include ../subproject.mk
