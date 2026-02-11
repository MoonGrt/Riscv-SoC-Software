# make clean && make -j $(nproc) && make mem

######################################
# Project config
######################################

PROJNAME := lvgl
OBJDIR   := build
MEMSIZE  := 65536

DEBUG    ?= yes
BENCH    ?= no
FUNCOPT  ?= yes
MULDIV   ?= yes
STDLIB   ?= no
MATHLIB  ?= no

######################################
# Directory layout
######################################

# SDK directory
SDK := ../../sdk
# Linker path
LINKER := ./linker.ld

######################################
# Source files
######################################

# Public library source code
LIB_DIR := $(SDK)/lib
LIB_SRCS := $(notdir $(wildcard $(LIB_DIR)/*.c))
# Standard library source code
STD_DIR := $(SDK)/std
STD_SRCS := $(notdir $(wildcard $(STD_DIR)/*.c))

# LVGL source code
LVGL_DIR := lvgl
LVGL_SRCS := $(wildcard $(LVGL_DIR)/port/*.c) \
             $(shell find $(LVGL_DIR)/src -name '*.c')

# Project source code
SRC_DIR := src
SRC_CPP_SRCS := $(shell find $(SRC_DIR) -name '*.cpp')
SRC_C_SRCS := $(shell find $(SRC_DIR) -name '*.c')
SRC_S_SRCS := $(shell find $(SRC_DIR) -name '*.S')

SRC_SRCS := $(SRC_CPP_SRCS) $(SRC_C_SRCS) $(SRC_S_SRCS) $(LVGL_SRCS)

######################################
# Object files layout
######################################

LIB_OBJS := $(addprefix $(OBJDIR)/lib/, $(LIB_SRCS:.c=.o))
STD_OBJS := $(addprefix $(OBJDIR)/lib/, $(STD_SRCS:.c=.o))

SRC_OBJS := $(addprefix $(OBJDIR)/, $(SRC_SRCS))
SRC_OBJS := $(SRC_OBJS:.cpp=.o)
SRC_OBJS := $(SRC_OBJS:.c=.o)
SRC_OBJS := $(SRC_OBJS:.S=.o)

OBJS := $(LIB_OBJS) $(STD_OBJS) $(SRC_OBJS)
DIRS := $(sort $(dir $(OBJS)))

######################################
# Include paths & Search paths
######################################

# Include paths
INC += -I$(LIB_DIR) -I$(STD_DIR)
INC += -I./lvgl -I./lvgl/port -I./lvgl/example
INC += -I./lvgl/src/core -I./lvgl/src/draw -I./lvgl/src/extra -I./lvgl/src/font \
	   -I./lvgl/src/hal -I./lvgl/src/misc -I./lvgl/src/widgets
INC += $(addprefix -I, $(shell find $(SRC_DIR) -type d))
# Search paths
VPATH += $(LIB_DIR) $(STD_DIR) $(LVGL_DIR) $(SRC_DIR)

######################################
# build.mk
######################################

include $(SDK)/build.mk
