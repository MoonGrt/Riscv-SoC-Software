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
LDFLAGS += -nostartfiles -lgcc -mcmodel=medany -ffreestanding\
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
	@$(SDK)/InstExtractor.sh $< $(MEMDIR)/$(PROJ_NAME) $(MEMSIZE) $(MEMTYPE) $(EXTRTEMP)

clean:
	rm -rf $(OBJDIR)

.SECONDARY: $(OBJS)

$(DIRS):
	@mkdir -p $@

######################################
# Link
######################################

$(OBJDIR)/$(PROJ_NAME).elf: $(OBJS) | $(DIRS)
	@echo "\n-----------------------------\n"
	$(RISCV_CC) $(CFLAGS) -o $@ $^ $(LDFLAGS)
	@echo "\n-----------------------------\n"

######################################
# Compile rules
######################################

$(OBJDIR)/lib/%.o: %.c | $(DIRS)
	$(RISCV_CC) -c $(CFLAGS) $(INC) -o $@ $<

$(OBJDIR)/%.o: %.c | $(DIRS)
	$(RISCV_CC) -c $(CFLAGS) $(INC) -o $@ $<

$(OBJDIR)/%.o: %.cpp | $(DIRS)
	$(RISCV_CC) -c $(CFLAGS) $(INC) -o $@ $<

$(OBJDIR)/%.o: %.S | $(DIRS)
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
