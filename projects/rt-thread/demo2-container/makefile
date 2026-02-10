# make clean && make -j $(nproc) && make mem

######################################
# Project config
######################################

PROJ_NAME := container
OBJDIR    := build
MEMSIZE   := 16384

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

# RT-Thread source code
RTTHREAD_DIR := rt-thread
RTTHREAD_C_SRCS := \
    $(shell find $(RTTHREAD_DIR)/libcpu -maxdepth 1 -name '*.c') \
    $(shell find $(RTTHREAD_DIR)/src -name '*.c')
RTTHREAD_S_SRCS := \
	$(shell find $(RTTHREAD_DIR)/libcpu -name '*.S')

# User source code
USER_DIR := user
USER_CPP_SRCS := $(shell find $(USER_DIR) -name '*.cpp')
USER_C_SRCS := $(shell find $(USER_DIR) -name '*.c')
USER_S_SRCS := $(shell find $(USER_DIR) -name '*.S')

SRC_SRCS := $(USER_CPP_SRCS) $(USER_C_SRCS) $(USER_S_SRCS) $(RTTHREAD_C_SRCS) $(RTTHREAD_S_SRCS)

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
INC += $(addprefix -I, $(shell find $(RTTHREAD_DIR) -type d))
INC += $(addprefix -I, $(shell find $(USER_DIR) -type d))
# Search paths
VPATH += $(LIBS)
VPATH += $(RTTHREAD_DIR)
VPATH += $(USER_DIR)

######################################
# build.mk
######################################

include ../build.mk
