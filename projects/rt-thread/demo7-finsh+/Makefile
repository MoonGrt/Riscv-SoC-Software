# make clean && make

PROJ_NAME = finsh
DEBUG = yes
BENCH = no
FUNC_OPT = yes
MULDIV = yes

SRCS = $(wildcard libs/*.c) \
       $(wildcard user/*.c) \
       $(wildcard user/*.S) \
       $(wildcard rt-thread/libcpu/*.c) \
       $(wildcard rt-thread/libcpu/*.S) \
       $(wildcard rt-thread/src/*.c) \
       $(wildcard rt-thread/components/finsh/*.c)

INC += -I./libs -I./rt-thread/include -I./rt-thread/libcpu -I./user -I./rt-thread/components/finsh
LDSCRIPT = link.lds

include ../gcc.mk

ifeq ($(DEBUG), yes)
	CFLAGS += -g3 -O0
else
	CFLAGS += -g -O3
endif

ifeq ($(BENCH), yes)
	CFLAGS += -fno-inline
endif

# 控制函数优化的选项
ifeq ($(FUNC_OPT), yes)
	CFLAGS += -ffunction-sections -fdata-sections
	LDFLAGS += -Wl,--gc-sections
else
	CFLAGS += -fno-function-sections -fno-data-sections
endif

ifeq ($(SIFIVE_GCC_PACK), yes)
	RISCV_CLIB=$(RISCV_PATH)/$(RISCV_NAME)/lib/$(MARCH)/$(MABI)/
else
	RISCV_CLIB=$(RISCV_PATH)/$(RISCV_NAME)/lib/
endif



RISCV_OBJCOPY = $(RISCV_PATH)/bin/$(RISCV_NAME)-objcopy
RISCV_OBJDUMP = $(RISCV_PATH)/bin/$(RISCV_NAME)-objdump
RISCV_CC=$(RISCV_PATH)/bin/$(RISCV_NAME)-gcc

CFLAGS += -MD -fstrict-volatile-bitfields
LDFLAGS += -lgcc -mcmodel=medany -nostartfiles -ffreestanding -Wl,-Bstatic,-T,$(LDSCRIPT),-Map,$(OBJDIR)/$(PROJ_NAME).map,--print-memory-usage

OBJDIR = build
OBJS := $(SRCS)
OBJS := $(OBJS:.c=.o)
OBJS := $(OBJS:.cpp=.o)
OBJS := $(OBJS:.S=.o)
OBJS := $(addprefix $(OBJDIR)/,$(OBJS))

all: $(OBJDIR)/$(PROJ_NAME).elf $(OBJDIR)/$(PROJ_NAME).hex $(OBJDIR)/$(PROJ_NAME).asm $(OBJDIR)/$(PROJ_NAME).v
	@echo "\nBuild successful for project: $(PROJ_NAME)\n"  # Add success message
	@echo "Output: $(shell pwd)/$(OBJDIR)/$(PROJ_NAME).elf"

%.bin: %.elf
	$(RISCV_OBJCOPY) -O binary $^ $@

%.hex: %.elf
	$(RISCV_OBJCOPY) -O ihex $^ $@

%.v: %.elf
	$(RISCV_OBJCOPY) -O verilog $^ $@

%.asm: %.elf
	$(RISCV_OBJDUMP) -S -d $^ > $@

$(OBJDIR):
	mkdir -p $@

$(OBJDIR)/%.elf: $(OBJS) | $(OBJDIR)
	@echo "\n---------\n"
	$(RISCV_CC) $(CFLAGS) -o $@ $^ $(LDFLAGS) $(LIBS)
	@echo "\n---------\n"

$(OBJDIR)/%.o: %.c
	mkdir -p $(dir $@)
	$(RISCV_CC) -c $(CFLAGS) $(INC) -o $@ $^

$(OBJDIR)/%.o: %.cpp
	mkdir -p $(dir $@)
	$(RISCV_CC) -c $(CFLAGS) $(INC) -o $@ $^

$(OBJDIR)/%.o: %.S
	mkdir -p $(dir $@)
	$(RISCV_CC) -c $(CFLAGS) -o $@ $^ -D__ASSEMBLY__=1

clean:
	rm -rf $(OBJDIR)/*

.SECONDARY: $(OBJS)

