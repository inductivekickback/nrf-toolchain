# The PROJECT_NAME can be changed arbitrarily (it does not depend on anything).
PROJECT_NAME := ble_app_uart_s130_pca10028

# The LINKER_SCRIPT is usually in the same directory as the Makefile.
LINKER_SCRIPT := ble_app_uart_gcc_nrf51.ld

BOARD := PCA10028

DBG_BUILD_DIR := ./_debug
REL_BUILD_DIR := ./_release
DEPS_DIR := ./_deps

# Init commands will be written to a file and then specified when starting GDB
# instead of relying on .gdbinit (to avoid having to enable .gbdinit files).
GDB_CMD_PATH := $(DBG_BUILD_DIR)/gdb.txt

SD_HEX_PATH := ../../../../../../components/softdevice/s130/hex/s130_nrf51_2.0.0_softdevice.hex

# Include the correct template Makefile depending on platform.
TEMPLATE_PATH = ../../../../../../components/toolchain/gcc
ifeq ($(OS),Windows_NT)
	include $(TEMPLATE_PATH)/Makefile.windows
# The -e option doesn't work in cygwin so -c is used and the job is placed
# in the background.
	TERMINAL := sh -c
	BG_JOB := &
	NRFJPROG := c:/Program Files (x86)/Nordic Semiconductor/nrf5x/bin/nrfjprog.exe
	GDBSERVER := c:/Program Files (x86)/SEGGER/JLink_V512e/JLinkGDBServer.exe
else
	include $(TEMPLATE_PATH)/Makefile.posix
	TERMINAL := gnome-terminal -e
	BG_JOB :=
	NRFJPROG := nrfjprog
	GDBSERVER := JLinkGDBServer
endif

# If multiple J-Links are attached to the computer then "SN=1234" can be used
# to specify a serial number for GDB and flash targets. A random GDB port will
# be generated so multiple targets can be debugged simultaneously.
GDB_PORT := 2331
ifdef SN
	NRFJPROG_SN := --snr $(SN)
	GDB_SERVER_SN := -select usb=$(SN)
	GDB_PORT := $(shell awk 'BEGIN{srand();printf("%4.4s", 1000+9999*rand())}')
endif

# Toolchain commands (these rely on the inclusion of the template Makefile)
CC := $(GNU_INSTALL_ROOT)/bin/$(GNU_PREFIX)-gcc
AS := $(GNU_INSTALL_ROOT)/bin/$(GNU_PREFIX)-as
AR := $(GNU_INSTALL_ROOT)/bin/$(GNU_PREFIX)-ar -r
LD := $(GNU_INSTALL_ROOT)/bin/$(GNU_PREFIX)-ld
NM := $(GNU_INSTALL_ROOT)/bin/$(GNU_PREFIX)-nm
OBJDUMP := $(GNU_INSTALL_ROOT)/bin/$(GNU_PREFIX)-objdump
OBJCOPY := $(GNU_INSTALL_ROOT)/bin/$(GNU_PREFIX)-objcopy
SIZE := $(GNU_INSTALL_ROOT)/bin/$(GNU_PREFIX)-size
GDB := $(GNU_INSTALL_ROOT)/bin/$(GNU_PREFIX)-gdb

SHAREDFLAGS += \
	-DNRF51 \
	-DNRF_LOG_USES_UART=1 \
	-DSWI_DISABLE0 \
	-DBOARD_$(BOARD) \
	-DS130 \
	-DSOFTDEVICE_PRESENT \
	-DBLE_STACK_SUPPORT_REQD

CFLAGS += \
	-mcpu=cortex-m0 \
	-mthumb \
	-mabi=aapcs \
	--std=gnu99 \
	-Wall \
	-Werror \
	-mfloat-abi=soft \
	-mfpu=fpv4-sp-d16 \
	-ffunction-sections \
	-fdata-sections \
	-fno-strict-aliasing \
	-fno-builtin \
	--short-enums \
	$(SHAREDFLAGS)

ASMFLAGS += \
	-x assembler-with-cpp \
	$(SHAREDFLAGS)

LDFLAGS += \
	-Xlinker \
	-Map=$(OBJ_DIR)/$(PROJECT_NAME).map \
	-mthumb \
	-mabi=aapcs \
	-L $(TEMPLATE_PATH) \
	-T$(LINKER_SCRIPT) \
	-mcpu=cortex-m0 \
	-Wl,--gc-sections \
	--specs=nano.specs \
	-lc \
	-lnosys

SRC_FILES += \
	../../../../../../components/libraries/button/app_button.c \
	../../../../../../components/libraries/util/app_error.c \
	../../../../../../components/libraries/util/app_error_weak.c \
	../../../../../../components/libraries/fifo/app_fifo.c \
	../../../../../../components/libraries/timer/app_timer.c \
	../../../../../../components/libraries/util/app_util_platform.c \
	../../../../../../components/libraries/fstorage/fstorage.c \
	../../../../../../components/libraries/util/nrf_assert.c \
	../../../../../../components/libraries/util/nrf_log.c \
	../../../../../../components/libraries/uart/retarget.c \
	../../../../../../components/libraries/uart/app_uart_fifo.c \
	../../../../../../components/drivers_nrf/delay/nrf_delay.c \
	../../../../../../components/drivers_nrf/common/nrf_drv_common.c \
	../../../../../../components/drivers_nrf/gpiote/nrf_drv_gpiote.c \
	../../../../../../components/drivers_nrf/uart/nrf_drv_uart.c \
	../../../../../../components/drivers_nrf/pstorage/pstorage.c \
	../../../../../../components/ble/common/ble_advdata.c \
	../../../../../../components/ble/ble_advertising/ble_advertising.c \
	../../../../../../components/ble/ble_services/ble_nus/ble_nus.c \
	../../../../../../components/ble/common/ble_conn_params.c \
	../../../../../../components/ble/common/ble_srv_common.c \
	../../../../../../components/toolchain/system_nrf51.c \
	../../../../../../components/softdevice/common/softdevice_handler/softdevice_handler.c \
	../../../../../../external/segger_rtt/RTT_Syscalls_GCC.c \
	../../../../../../external/segger_rtt/SEGGER_RTT.c \
	../../../../../../external/segger_rtt/SEGGER_RTT_printf.c \
	../../../../../bsp/bsp.c \
	../../../../../bsp/bsp_btn_ble.c \
	../../../main.c

ASM_FILES += \
	../../../../../../components/toolchain/gcc/gcc_startup_nrf51.s

INC_DIRS += \
	../../../../../../components/libraries/timer \
	../../../../../../components/libraries/fifo \
	../../../../../../components/libraries/fstorage/config \
	../../../../../../components/drivers_nrf/delay \
	../../../../../../components/softdevice/s130/headers/nrf51 \
	../../../../../../components/libraries/util \
	../../../../../../components/drivers_nrf/uart \
	../../../../../../components/ble/common \
	../../../../../../components/drivers_nrf/pstorage \
	../../../../../../components/device \
	../../../../../../components/libraries/uart \
	../../../../../../components/libraries/button \
	../../../../../../components/libraries/fstorage \
	../../../../../../components/libraries/experimental_section_vars \
	../../../../../../components/softdevice/s130/headers \
	../../../../../../components/drivers_nrf/gpiote \
	../../../../../../components/toolchain/CMSIS/Include \
	../../../../../../components/drivers_nrf/hal \
	../../../../../../components/toolchain/gcc \
	../../../../../../components/toolchain \
	../../../../../../components/drivers_nrf/common \
	../../../../../../components/ble/ble_advertising \
	../../../../../../components/softdevice/common/softdevice_handler \
	../../../../../../components/ble/ble_services/ble_nus \
	../../../../../../external/segger_rtt \
	../../../../../bsp \
	../../../config/ble_app_uart_s130_pca10028 \
	../../../config \

# Convert to absolute paths and sort to remove duplicates.
SRC_FILES := $(sort $(foreach f,$(SRC_FILES),$(abspath $(f))))
INC_DIRS := $(sort $(foreach d,$(INC_DIRS),$(abspath $(d))))

# This directory needs to be added after the main list is sorted because it
# contains its own copy of 'nrf_drv_config.h' that will conflict with the
# project's local version if it's found first.
INC_DIRS += $(abspath ../../../../../../components/drivers_nrf/config)

SRC_DIRS := $(dir $(SRC_FILES) $(ASM_FILES))

SRC_FILE_NAMES := $(notdir $(SRC_FILES) $(ASM_FILES))

# Convert each source file name into the form '$(OBJ_DIR)/$(SRC_FILE).o'.
OBJ := $(patsubst %,%.o,$(basename $(SRC_FILE_NAMES)))
DBG_OBJ := $(addprefix $(DBG_BUILD_DIR)/,$(OBJ))
REL_OBJ := $(addprefix $(REL_BUILD_DIR)/,$(OBJ))

.PHONY: default
default: CFLAGS += -O0 -ggdb
default: OBJ_DIR := $(DBG_BUILD_DIR)
default: $(DBG_BUILD_DIR)/$(PROJECT_NAME).hex
	$(call echosize,$(DBG_BUILD_DIR)/$(PROJECT_NAME).out)

.PHONY: release
release: CFLAGS += -O3 -g3
release: OBJ_DIR := $(REL_BUILD_DIR)
release: $(REL_BUILD_DIR)/$(PROJECT_NAME).bin $(REL_BUILD_DIR)/$(PROJECT_NAME).hex
	$(call echosize,$(REL_BUILD_DIR)/$(PROJECT_NAME).out)

.PHONY: all
all: default release

DBG_DEP := $(addprefix $(DEPS_DIR)/,$(OBJ:.o=.d))
-include $(DBG_DEP)

INCLUDES := $(patsubst %,-I%,$(INC_DIRS))

vpath %.c $(SRC_DIRS)
vpath %.s $(SRC_DIRS)

define echosize
	@echo ''
	@'$(SIZE)' $1;
	@echo ''
endef

define flash
	@"$(NRFJPROG)" $(NRFJPROG_SN) --program $1 -f nrf51 --sectorerase --verify
	@"$(NRFJPROG)" $(NRFJPROG_SN) --reset -f nrf51
endef

$(DBG_BUILD_DIR)/%.o: %.c | $(DBG_BUILD_DIR)
	@echo Compiling file: $(notdir $<)
	@'$(CC)' $(CFLAGS) $(INCLUDES) -c -o $@ $<

$(DBG_BUILD_DIR)/%.o: %.s | $(DBG_BUILD_DIR)
	@echo Compiling file: $(notdir $<)
	@'$(CC)' $(ASMFLAGS) $(INCLUDES) -c -o $@ $<

$(DBG_BUILD_DIR)/$(PROJECT_NAME).hex: $(DBG_BUILD_DIR)/$(PROJECT_NAME).out
	@echo Creating hex file: $(notdir $@)
	@'$(OBJCOPY)' -O ihex $(DBG_BUILD_DIR)/$(PROJECT_NAME).out $@

$(DBG_BUILD_DIR)/$(PROJECT_NAME).bin: $(DBG_BUILD_DIR)/$(PROJECT_NAME).out
	@echo Creating bin file: $(notdir $@)
	@'$(OBJCOPY)' -O binary $(DBG_BUILD_DIR)/$(PROJECT_NAME).out $@

$(DBG_BUILD_DIR)/$(PROJECT_NAME).out: $(DBG_OBJ)
	@echo Linking ELF file: $(notdir $@)
	@'$(CC)' $(LDFLAGS) $(DBG_OBJ) -lm -o $@

$(REL_BUILD_DIR)/%.o: %.c | $(REL_BUILD_DIR)
	@echo Compiling file: $(notdir $<)
	@'$(CC)' $(CFLAGS) $(INCLUDES) -c -o $@ $<

$(REL_BUILD_DIR)/%.o: %.s | $(REL_BUILD_DIR)
	@echo Compiling file: $(notdir $<)
	@'$(CC)' $(ASMFLAGS) $(INCLUDES) -c -o $@ $<

$(REL_BUILD_DIR)/$(PROJECT_NAME).hex: $(REL_BUILD_DIR)/$(PROJECT_NAME).out
	@echo Creating hex file: $(notdir $@)
	@'$(OBJCOPY)' -O ihex $(REL_BUILD_DIR)/$(PROJECT_NAME).out $@

$(REL_BUILD_DIR)/$(PROJECT_NAME).bin: $(REL_BUILD_DIR)/$(PROJECT_NAME).out
	@echo Creating bin file: $(notdir $@)
	@'$(OBJCOPY)' -O binary $(REL_BUILD_DIR)/$(PROJECT_NAME).out $@

$(REL_BUILD_DIR)/$(PROJECT_NAME).out: $(REL_OBJ)
	@echo Linking ELF file: $(notdir $@)
	@'$(CC)' $(LDFLAGS) $(REL_OBJ) -lm -o $@

$(DEPS_DIR)/%.d: %.c | $(DEPS_DIR)
	@echo Adding dependency for file: $(notdir $<)
	@echo -n "$(DBG_BUILD_DIR)/$(notdir $(<:.c=.o)) " > $@
	@'$(CC)' $(CFLAGS) $(INCLUDES) -c $< -MM \
		-MT $(REL_BUILD_DIR)/$(notdir $(<:.c=.o)) >> $@

$(DEPS_DIR)/%.d: %.s | $(DEPS_DIR)
	@echo Adding dependency for file: $(notdir $<)
	@echo -n "$(DBG_BUILD_DIR)/$(notdir $(<:.c=.o)) " > $@
	@'$(CC)' $(ASMFLAGS) $(INCLUDES) -c $< -MM \
		-MT $(REL_BUILD_DIR)/$(notdir $(<:.c=.o)) >> $@

$(DEPS_DIR) $(DBG_BUILD_DIR) $(REL_BUILD_DIR):; @mkdir $@

.PHONY: flash_sd
flash_sd:
	$(call flash,$(SD_HEX_PATH))

.PHONY: flash_debug
flash_debug: default
	$(call flash,$(DBG_BUILD_DIR)/$(PROJECT_NAME).hex)

.PHONY: flash_release
flash_release: release
	$(call flash,$(REL_BUILD_DIR)/$(PROJECT_NAME).hex)

.PHONY: gdb
gdb: ELF_PATH = "$(DBG_BUILD_DIR)/$(PROJECT_NAME).out"
gdb: default
	@$(TERMINAL) "'$(GDBSERVER)' $(GDB_SERVER_SN) -device nrf51 \
		-if swd -port $(GDB_PORT)" $(BG_JOB)
	@echo "target remote localhost:$(GDB_PORT)" > $(GDB_CMD_PATH)
	@echo "break main" >> $(GDB_CMD_PATH)
	@echo "mon speed 10000" >> $(GDB_CMD_PATH)
	@echo "mon flash download= 1" >> $(GDB_CMD_PATH)
	@echo "load $(ELF_PATH)" >> $(GDB_CMD_PATH)
	@echo "mon reset 0" >> $(GDB_CMD_PATH)
	@$(TERMINAL) "'$(GDB)' $(ELF_PATH) -x $(GDB_CMD_PATH)"

.PHONY: clean
clean:
	@rm -rf $(DBG_BUILD_DIR)
	@rm -rf $(REL_BUILD_DIR)
	@rm -rf $(DEPS_DIR)

.PHONY: help
help:
	@echo "The following targets are available:"
	@echo "    (default)              - Compile with debug flags"
	@echo "    release                - Compile with release flags"
	@echo "    all                    - Compile debug and release targets"
	@echo "    clean                  - Remove object and dependency directories"
	@echo "    gdb [SN=1234]          - Perform debug compile and then launch gdb"
	@echo "    flash_sd [SN=1234]     - Flash the SoftDevice"
	@echo "    flash_debug [SN=1234]  - Flash the debug build"
	@echo "    flash_release [SN=1234]- Flash the release build"

# This is a special target that tells make to delete a file if an error occurs
# while the file is being generated.
.DELETE_ON_ERROR:
