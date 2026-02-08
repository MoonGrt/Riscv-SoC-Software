# make clean && make -j $(nproc) && make mem

######################################
# Project config
######################################

PROJ_NAME := boot
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

# Project source code
SRC_DIR := src
SRC_CPP_SRCS := $(shell find $(SRC_DIR) -name '*.cpp')
SRC_C_SRCS := $(shell find $(SRC_DIR) -name '*.c')
SRC_S_SRCS := $(shell find $(SRC_DIR) -name '*.S')
SRC_SRCS := $(SRC_CPP_SRCS) $(SRC_C_SRCS) $(SRC_S_SRCS)

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
INC += $(addprefix -I, $(shell find $(SRC_DIR) -type d))
# Search paths
VPATH += $(LIBS)
VPATH += $(SRC_DIR)

######################################
# build.mk
######################################

include ../build.mk
