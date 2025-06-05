# make clean && make

PROJ_NAME = lcd
DEBUG = yes
BENCH = no
FUNC_OPT = yes
MULDIV = yes

SRCS = $(wildcard libs/*.c) \
       $(wildcard libs/*.S) \
       $(wildcard src/*.c) \
       $(wildcard src/*.S) \
       $(wildcard src/ov5640/*.c) \

INC += -I./libs -I./src -I./src/ov5640
LDSCRIPT = linker.ld

include ../gcc.mk
include ../subproject.mk
