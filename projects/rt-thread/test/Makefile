# make clean && make

PROJ_NAME = test
DEBUG = yes
BENCH = no
FUNC_OPT = yes
MULDIV = yes

SRCS = $(wildcard libs/*.c) \
       $(wildcard user/*.c) \
       $(wildcard user/*.S) \
       $(wildcard rt-thread/libcpu/*.c) \
       $(wildcard rt-thread/libcpu/*.S) \
       $(wildcard rt-thread/src/*.c) \
       $(wildcard rt-thread/components/finsh/*.c) \
       $(wildcard rt-thread/components/dfs/*.c) \
       $(wildcard user/ov5640/*.c)

INC += -I./libs -I./rt-thread/include -I./rt-thread/libcpu -I./user -I./rt-thread/components/finsh -I./user/ov5640 -I./rt-thread/components/dfs
LDSCRIPT = link.lds

include ../gcc.mk
include ../subproject.mk
