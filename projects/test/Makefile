# make clean && make

PROJ_NAME = test
DEBUG = no
BENCH = no
FUNC_OPT = yes
MULDIV = yes

SRCS = $(wildcard libs/*.c) \
       $(wildcard libs/*.S) \
       $(wildcard src/*.c) \
       $(wildcard src/*.S)

INC += -I./libs -I./src
LDSCRIPT = linker.ld

include ../../resources/gcc.mk
include ../../resources/subproject.mk
