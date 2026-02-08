# make clean && make -j $(nproc) && make mem

######################################
# Project config
######################################

PROJ_NAME := dvp
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
SRC_C_SRCS := $(shell find $(SRC_DIR) -name '*.c')
SRC_S_SRCS := $(shell find $(SRC_DIR) -name '*.S')
SRC_SRCS := $(SRC_C_SRCS) $(SRC_S_SRCS)

######################################
# Object files layout
######################################

LIB_OBJS := $(addprefix $(OBJDIR)/libs/, $(LIB_SRCS:.c=.o))
SRC_OBJS := $(SRC_SRCS:$(SRC_DIR)/%=$(OBJDIR)/$(SRC_DIR)/%)
SRC_OBJS := $(SRC_OBJS:.c=.o)
SRC_OBJS := $(SRC_OBJS:.S=.o)
OBJS := $(LIB_OBJS) $(SRC_OBJS)

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
# Toolchain
######################################

# Set it to yes if you are using the sifive precompiled GCC pack
SIFIVE_GCC_PACK ?= yes

ifeq ($(SIFIVE_GCC_PACK),yes)
    RISCV_NAME ?= riscv64-unknown-elf
    RISCV_PATH ?= /opt/riscv
else
    RISCV_NAME ?= riscv32-unknown-elf
    ifeq ($(MULDIV),yes)
        RISCV_PATH ?= /opt/riscv32im
    else
        RISCV_PATH ?= /opt/riscv32i
    endif
endif

RISCV_CC      := $(RISCV_PATH)/bin/$(RISCV_NAME)-gcc
RISCV_OBJCOPY := $(RISCV_PATH)/bin/$(RISCV_NAME)-objcopy
RISCV_OBJDUMP := $(RISCV_PATH)/bin/$(RISCV_NAME)-objdump

######################################
# ISA / ABI
######################################

MABI=ilp32
MARCH := rv32i
ifeq ($(MULDIV),yes)
    MARCH := $(MARCH)m
endif
ifeq ($(COMPRESSED),yes)
    MARCH := $(MARCH)ac
endif

CFLAGS += -march=$(MARCH) -mabi=$(MABI)
# LDFLAGS += -march=$(MARCH) -mabi=$(MABI)

######################################
# Flags
######################################

ifeq ($(DEBUG),yes)
    CFLAGS += -g3 -O0
else
    CFLAGS += -g -O3
endif

ifeq ($(BENCH), yes)
    CFLAGS += -fno-inline
endif

ifeq ($(FUNC_OPT), yes)
    CFLAGS += -ffunction-sections -fdata-sections
    LDFLAGS += -Wl,--gc-sections
else
    CFLAGS += -fno-function-sections -fno-data-sections
endif

CFLAGS  += -MD -fstrict-volatile-bitfields
LDFLAGS += -nostdlib -nostartfiles -lgcc -mcmodel=medany\
           -Wl,-Bstatic,-T,$(LINKER) \
           -Wl,-Map,$(OBJDIR)/$(PROJ_NAME).map,--print-memory-usage

######################################
# Targets
######################################

.PHONY: all

all: $(OBJDIR)/$(PROJ_NAME).elf \
     $(OBJDIR)/$(PROJ_NAME).hex \
     $(OBJDIR)/$(PROJ_NAME).asm \
     $(OBJDIR)/$(PROJ_NAME).v
	@echo "\nBuild successful for project: $(PROJ_NAME)\n"
	@echo "Output: $(shell pwd)/$(OBJDIR)/$(PROJ_NAME).elf"

MEMDIR   := $(OBJDIR)/mem
MEMTYPE  := bin
EXTRTEMP := true
mem: $(OBJDIR)/$(PROJ_NAME).hex
	@echo "\nGenerating .mem from .hex..."
	mkdir -p $(MEMDIR)
	@../../scripts/InstExtractor.sh $< $(MEMDIR)/$(PROJ_NAME) $(MEMSIZE) $(MEMTYPE) $(EXTRTEMP)

clean:
	rm -rf $(OBJDIR)

.SECONDARY: $(OBJS)

$(OBJDIR):
	mkdir -p $@

######################################
# Link
######################################

$(OBJDIR)/$(PROJ_NAME).elf: $(OBJS) | $(OBJDIR)
	@echo "\n-----------------------------\n"
	$(RISCV_CC) $(CFLAGS) -o $@ $^ $(LDFLAGS)
	@echo "\n-----------------------------\n"

######################################
# Compile rules
######################################

$(OBJDIR)/libs/%.o: %.c
	mkdir -p $(dir $@)
	$(RISCV_CC) -c $(CFLAGS) $(INC) -o $@ $<

$(OBJDIR)/src/%.o: %.c
	mkdir -p $(dir $@)
	$(RISCV_CC) -c $(CFLAGS) $(INC) -o $@ $<

$(OBJDIR)/src/%.o: %.cpp
	mkdir -p $(dir $@)
	$(RISCV_CC) -c $(CFLAGS) $(INC) -o $@ $<

$(OBJDIR)/src/%.o: %.S
	mkdir -p $(dir $@)
	$(RISCV_CC) -c $(CFLAGS) -D__ASSEMBLY__=1 -o $@ $<

######################################
# Output formats
######################################

%.bin: %.elf
	$(RISCV_OBJCOPY) -O binary $^ $@

%.hex: %.elf
	$(RISCV_OBJCOPY) -O ihex $^ $@

%.v: %.elf
	$(RISCV_OBJCOPY) -O verilog $^ $@

%.asm: %.elf
	$(RISCV_OBJDUMP) -S -d $^ > $@
