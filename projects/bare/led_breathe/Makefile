# make clean && make

PROJ_NAME = led_breathe
DEBUG = yes
BENCH = no
FUNC_OPT = yes
MULDIV = yes

SRCS = $(wildcard libs/*.c) \
       $(wildcard libs/*.S) \
       $(wildcard src/*.c) \
       $(wildcard src/*.S)

INC += -I./libs -I./src
LDSCRIPT = linker.ld

include ../gcc.mk
include ../subproject.mk
