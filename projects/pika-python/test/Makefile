# make clean && make

PROJ_NAME = test
DEBUG = no
BENCH = no
FUNC_OPT = yes
MULDIV = yes

SRCS = $(wildcard libs/*.c) \
       $(wildcard libs/*.S) \
       $(wildcard src/*.c) \
       $(wildcard src/*.S) \
       $(wildcard src/ov5640/*.c) \
       $(wildcard pikapython/pikascript-api/*.c) \
       $(wildcard pikapython/pikascript-core/*.c) \
       $(wildcard pikapython/pikascript-lib/PikaStdDevice/*.c) \
       $(wildcard pikapython/pikascript-lib/PikaStdLib/*.c) \

INC += -I./libs -I./src -I./src/ov5640 -I./pikapython/pikascript-api -I./pikapython/pikascript-core -I./pikapython/pikascript-lib/PikaStdLib
LDSCRIPT = linker.ld

include ../gcc.mk
include ../subproject.mk
