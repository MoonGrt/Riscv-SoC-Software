# make clean && make

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
       $(wildcard lvgl/src/core/*.c) \
       $(wildcard lvgl/src/draw/*.c) \
       $(wildcard lvgl/src/extra/*.c) \
       $(wildcard lvgl/src/font/*.c) \
       $(wildcard lvgl/src/hal/*.c) \
       $(wildcard lvgl/src/misc/*.c) \
       $(wildcard lvgl/src/widgets/*.c) \
       $(wildcard lvgl/port/*.c) \
       $(wildcard lvgl/app/*.c) \

INC += -I./libs -I./libc -I./src
INC += -I./lvgl -I./lvgl/port -I./lvgl/example
INC += -I./lvgl/src/core -I./lvgl/src/draw -I./lvgl/src/extra -I./lvgl/src/font -I./lvgl/src/hal -I./lvgl/src/misc -I./lvgl/src/widgets
INC += -I./lvgl/src/draw/arm2d -I./lvgl/src/draw/nxp -I./lvgl/src/draw/renesas -I./lvgl/src/draw/sdl -I./lvgl/src/draw/sw
INC += -I./lvgl/src/extra/layouts -I./lvgl/src/extra/libs -I./lvgl/src/extra/others -I./lvgl/src/extra/themes -I./lvgl/src/extra/widgets
LDSCRIPT = linker.ld

include ../gcc.mk
include ../subproject.mk

