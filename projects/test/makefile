# make clean && make

PROJ_NAME = test
DEBUG = no
BENCH = no
FUNC_OPT = yes
MULDIV = no

SRCS = $(wildcard libs/*.c) \
       $(wildcard libs/*.cpp) \
       $(wildcard libs/*.S) \
       $(wildcard src/*.c) \
       $(wildcard src/*.cpp) \
       $(wildcard src/*.S)

INC += -I./libs -I./src
LDSCRIPT = linker.ld

include ../../resources/gcc.mk
include ../../resources/subproject.mk
