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
       $(shell find lvgl -name "*.c")
       # $(wildcard lvgl/src/core/*.c) \
       # $(wildcard lvgl/src/draw/*.c) \
       # $(wildcard lvgl/src/draw/arm2d/*.c) \
       # $(wildcard lvgl/src/draw/nxp_pxp/*.c) \
       # $(wildcard lvgl/src/draw/nxp_vglite/*.c) \
       # $(wildcard lvgl/src/draw/sdl/*.c) \
       # $(wildcard lvgl/src/draw/sw/*.c) \
       # $(wildcard lvgl/src/extra/*.c) \
       # $(wildcard lvgl/src/extra/layouts/flex/*.c) \
       # $(wildcard lvgl/src/extra/layouts/grid/*.c) \
       # $(wildcard lvgl/src/extra/themes/default/*.c) \
       # $(wildcard lvgl/src/font/*.c) \
       # $(wildcard lvgl/src/hal/*.c) \
       # $(wildcard lvgl/src/misc/*.c) \
       # $(wildcard lvgl/src/widgets/*.c) \
       # $(wildcard lvgl/port/*.c) \
       # $(wildcard lvgl/app/*.c) \

INC += -I./libs -I./libc -I./src
INC += -I./lvgl -I./lvgl/port -I./lvgl/example
INC += -I./lvgl/src/core -I./lvgl/src/draw -I./lvgl/src/extra -I./lvgl/src/font -I./lvgl/src/hal -I./lvgl/src/misc -I./lvgl/src/widgets
LDSCRIPT = linker.ld

include ../gcc.mk
include ../subproject.mk

