# make clean && make -j $(nproc)

PROJ_NAME = lvgl
DEBUG = no
BENCH = no
FUNC_OPT = yes
MULDIV = yes

SRCS = $(wildcard libs/*.c) \
       $(wildcard libs/*.S) \
       $(wildcard libc/*.c) \
       $(wildcard src/*.c) \
       $(wildcard src/*.S) \
       $(wildcard lvgl/port/*.c) \
       $(shell find lvgl/src -name "*.c") \

INC += -I./libs -I./libc -I./src
INC += -I./lvgl -I./lvgl/port -I./lvgl/example
INC += -I./lvgl/src/core -I./lvgl/src/draw -I./lvgl/src/extra -I./lvgl/src/font -I./lvgl/src/hal -I./lvgl/src/misc -I./lvgl/src/widgets
LDSCRIPT = linker.ld

include ../gcc.mk
include ../subproject.mk

