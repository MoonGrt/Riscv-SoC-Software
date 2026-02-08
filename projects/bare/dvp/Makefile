# make clean && make -j $(nproc) && make mem

######################################
# Project config
######################################

PROJ_NAME := test
OBJDIR    := build
MEMSIZE   := 8192

DEBUG     ?= yes
BENCH     ?= no
FUNC_OPT  ?= yes
MULDIV    ?= yes

######################################
# Directory layout
######################################

# Current directory
CURDIR  := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))
# Project root directory
ROOTDIR := $(abspath $(CURDIR)/../..)
# Public library directory
COMMON_LIBS := $(ROOTDIR)/libs
# Linker path
LDSCRIPT = ../linker.ld

######################################
# Source files
######################################

# Public library source code
LIB_C_SRCS := $(notdir $(wildcard $(COMMON_LIBS)/*.c))

# Project source code
SRC_DIR := src
SRC_C_SRCS := $(shell find $(SRC_DIR) -name '*.c')
SRC_S_SRCS := $(shell find $(SRC_DIR) -name '*.S')
SRC_SRCS := $(SRC_C_SRCS) $(SRC_S_SRCS)

######################################
# Include paths
######################################

INC += -I$(COMMON_LIBS)
INC += $(addprefix -I, $(shell find src -type d))

######################################
# Object files layout
######################################

LIB_OBJS := $(addprefix $(OBJDIR)/libs/, \
            $(LIB_C_SRCS:.c=.o) $(LIB_S_SRCS:.S=.o))
SRC_OBJS := $(SRC_SRCS:$(SRC_DIR)/%=$(OBJDIR)/src/%)
SRC_OBJS := $(SRC_OBJS:.c=.o)
SRC_OBJS := $(SRC_OBJS:.S=.o)
OBJS := $(LIB_OBJS) $(SRC_OBJS)

######################################
# Search path for sources
######################################

VPATH += $(COMMON_LIBS)
VPATH += src

######################################
# build.mk
######################################

include ../build.mk
