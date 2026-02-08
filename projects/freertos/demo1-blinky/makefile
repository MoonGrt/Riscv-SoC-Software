# make clean && make -j $(nproc) && make mem

######################################
# Project config
######################################

PROJ_NAME := blinky
OBJDIR    := build
MEMSIZE   := 8192

DEBUG     ?= yes
BENCH     ?= no
FUNC_OPT  ?= yes
MULDIV    ?= yes

######################################
# Directory layout
######################################

# Public library directory
LIBS := ../../libs
# Linker path
LINKER := ./linker.ld

######################################
# Source files
######################################

# Public library source code
LIB_SRCS := $(notdir $(wildcard $(LIBS)/*.c))

# Freertos source code
FREERTOS_DIR := freertos
FREERTOS_C_SRCS := \
    $(shell find $(FREERTOS_DIR)/src -maxdepth 1 -name '*.c') \
    $(shell find $(FREERTOS_DIR)/portable/RISC-V -name '*.c') \
    $(shell find $(FREERTOS_DIR)/portable/MemMang -name 'heap_1.c')
FREERTOS_S_SRCS := \
	$(shell find $(FREERTOS_DIR)/src -name '*.S') \
    $(shell find $(FREERTOS_DIR)/portable/RISC-V -name '*.S')

# User source code
USER_DIR := user
USER_CPP_SRCS := $(shell find $(USER_DIR) -name '*.cpp')
USER_C_SRCS := $(shell find $(USER_DIR) -name '*.c')
USER_S_SRCS := $(shell find $(USER_DIR) -name '*.S')

SRC_SRCS := $(USER_CPP_SRCS) $(USER_C_SRCS) $(USER_S_SRCS) $(FREERTOS_C_SRCS) $(FREERTOS_S_SRCS)

######################################
# Object files layout
######################################

LIB_OBJS := $(addprefix $(OBJDIR)/libs/, $(LIB_SRCS:.c=.o))
SRC_OBJS := $(addprefix $(OBJDIR)/, $(SRC_SRCS))
SRC_OBJS := $(SRC_OBJS:.cpp=.o)
SRC_OBJS := $(SRC_OBJS:.c=.o)
SRC_OBJS := $(SRC_OBJS:.S=.o)

OBJS := $(LIB_OBJS) $(SRC_OBJS)
DIRS := $(sort $(dir $(OBJS)))

######################################
# Include paths & Search paths
######################################

# Include paths
INC += -I$(LIBS)
INC += $(addprefix -I, $(shell find $(FREERTOS_DIR) -type d))
INC += $(addprefix -I, $(shell find $(USER_DIR) -type d))
# Search paths
VPATH += $(LIBS)
VPATH += $(FREERTOS_DIR)
VPATH += $(USER_DIR)

######################################
# build.mk
######################################

include ../build.mk
