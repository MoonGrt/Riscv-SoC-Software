# make clean && make

PROJ_NAME = lvgl
DEBUG = yes
BENCH = no
FUNC_OPT = yes
MULDIV = yes

SRCS = $(wildcard libs/*.c) \
       $(wildcard libs/*.S) \
       $(wildcard src/*.c) \
       $(wildcard src/*.S) \
       $(wildcard lvgl/src/*.c) \
       $(wildcard lvgl/src/core/*.c) \
       $(wildcard lvgl/src/draw/*.c) \
       $(wildcard lvgl/src/draw/dma2d/*.c) \
       $(wildcard lvgl/src/draw/nema_gfx/*.c) \
       $(wildcard lvgl/src/draw/nxp/*.c) \
       $(wildcard lvgl/src/draw/opengles/*.c) \
       $(wildcard lvgl/src/draw/renesas/*.c) \
       $(wildcard lvgl/src/draw/sdl/*.c) \
       $(wildcard lvgl/src/draw/sw/*.c) \
       $(wildcard lvgl/src/draw/vg_lite/*.c) \
       $(wildcard lvgl/src/font/*.c) \
       $(wildcard lvgl/src/hal*.c) \
       $(wildcard lvgl/src/misc/*.c) \
       $(wildcard lvgl/src/widgets/*.c) \
       

INC += -I./libs -I./src
INC += -I./lvgl -I./lvgl/src -I./lvgl/examples/porting
LDSCRIPT = linker.ld

include ../gcc.mk
include ../subproject.mk
