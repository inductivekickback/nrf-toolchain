# The PROJECT_NAME can be changed arbitrarily (it does not depend on anything).
PROJECT_NAME := ble_app_uart_s132_pca10040

# The LINKER_SCRIPT is usually in the same directory as the Makefile.
LINKER_SCRIPT := ble_app_uart_gcc_nrf52.ld

BOARD := PCA10040

DBG_BUILD_DIR := ./_debug
REL_BUILD_DIR := ./_release
DEPS_DIR := ./_deps

SDK_ROOT := ../../../../../..
PROJ_DIR := ../../..

# Init commands will be written to a file and then specified when starting GDB
# instead of relying on .gdbinit (to avoid having to enable .gbdinit files).
GDB_CMD_PATH := $(DBG_BUILD_DIR)/gdb.txt

SD_HEX_PATH := $(SDK_ROOT)/components/softdevice/s132/hex/s132_nrf52_4.0.2_softdevice.hex

# GDB needs to know the offset of the application when using Monitor Mode Debugging.
APP_FLASH_LOCATION := 0x1f000

# Include the correct template Makefile depending on platform.
TEMPLATE_PATH = $(SDK_ROOT)/components/toolchain/gcc
ifeq ($(OS),Windows_NT)
	include $(TEMPLATE_PATH)/Makefile.windows
# The -e option doesn't work in cygwin so -c is used and the job is placed
# in the background.
	TERMINAL := sh -c
	BG_JOB := &
	NRFJPROG := c:/Program Files (x86)/Nordic Semiconductor/nrf5x/bin/nrfjprog.exe
	RTT_CLIENT := c:/Program Files (x86)/SEGGER/JLink_V512e/JLinkRTTClient.exe
else
	include $(TEMPLATE_PATH)/Makefile.posix
	TERMINAL := gnome-terminal -e
	BG_JOB :=
	NRFJPROG := nrfjprog
	GDBSERVER := JLinkGDBServer
	RTT_CLIENT := JLinkRTTClient
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
	-mcpu=cortex-m4 \
	-mthumb \
	-DNRF52 \
	-DNRF52832_XXAA \
	-DCONFIG_GPIO_AS_PINRESET \
	-DSWI_DISABLE0 \
	-DBOARD_$(BOARD) \
	-DS132 \
	-DSOFTDEVICE_PRESENT \
	-DBLE_STACK_SUPPORT_REQD \
	-DNRF_SD_BLE_API_VERSION=4 \
	-DNRF52_PAN_74

CFLAGS += \
	--std=gnu99 \
	-Wall \
	-Werror \
	-mfloat-abi=hard \
	-mfpu=fpv4-sp-d16 \
	-ffunction-sections \
	-fdata-sections \
	-fno-strict-aliasing \
	-fno-builtin \
	--short-enums \
	-mabi=aapcs \
	$(SHAREDFLAGS)
ifdef MMD
	CFLAGS += -DMMD
endif

ASMFLAGS += \
	-x assembler-with-cpp \
	$(SHAREDFLAGS)

LDFLAGS += \
	-mthumb \
	-mabi=aapcs \
	-L $(TEMPLATE_PATH) \
	-T$(LINKER_SCRIPT) \
	-mcpu=cortex-m4 \
	-mfloat-abi=hard \
	-mfpu=fpv4-sp-d16 \
	-Wl,--gc-sections \
	--specs=nano.specs \
	-lc \
	-lnosys

SRC_FILES += \
	$(SDK_ROOT)/components/libraries/button/app_button.c \
	$(SDK_ROOT)/components/libraries/util/app_error.c \
	$(SDK_ROOT)/components/libraries/util/app_error_weak.c \
	$(SDK_ROOT)/components/libraries/fifo/app_fifo.c \
	$(SDK_ROOT)/components/libraries/timer/app_timer.c \
	$(SDK_ROOT)/components/libraries/uart/app_uart_fifo.c \
	$(SDK_ROOT)/components/libraries/util/app_util_platform.c \
	$(SDK_ROOT)/components/libraries/fstorage/fstorage.c \
	$(SDK_ROOT)/components/drivers_nrf/clock/nrf_drv_clock.c \
	$(SDK_ROOT)/components/drivers_nrf/common/nrf_drv_common.c \
	$(SDK_ROOT)/components/drivers_nrf/gpiote/nrf_drv_gpiote.c \
	$(SDK_ROOT)/components/drivers_nrf/uart/nrf_drv_uart.c \
	$(SDK_ROOT)/components/libraries/bsp/bsp.c \
	$(SDK_ROOT)/components/libraries/bsp/bsp_btn_ble.c \
	$(PROJ_DIR)/main.c \
	$(SDK_ROOT)/components/ble/common/ble_advdata.c \
	$(SDK_ROOT)/components/ble/ble_advertising/ble_advertising.c \
	$(SDK_ROOT)/components/ble/common/ble_conn_params.c \
	$(SDK_ROOT)/components/ble/common/ble_srv_common.c \
	$(SDK_ROOT)/components/toolchain/system_nrf52.c \
	$(SDK_ROOT)/components/ble/ble_services/ble_nus/ble_nus.c \
	$(SDK_ROOT)/components/softdevice/common/softdevice_handler/softdevice_handler.c \
	$(SDK_ROOT)/components/boards/boards.c \
	$(SDK_ROOT)/components/libraries/log/src/nrf_log_frontend.c \
	$(SDK_ROOT)/components/libraries/log/src/nrf_log_backend_serial.c \
	$(SDK_ROOT)/external/segger_rtt/RTT_Syscalls_GCC.c \
	$(SDK_ROOT)/external/segger_rtt/SEGGER_RTT.c \
	$(SDK_ROOT)/external/segger_rtt/SEGGER_RTT_printf.c \
	$(SDK_ROOT)/components/ble/nrf_ble_gatt/nrf_ble_gatt.c
ifdef MMD
	SRC_FILES += $(SDK_ROOT)/external/jlink_monitor_mode_debug/gcc/JLINK_MONITOR.c
endif

	ASM_FILES += $(SDK_ROOT)/components/toolchain/gcc/gcc_startup_nrf52.s
ifdef MMD
	ASM_FILES += $(SDK_ROOT)/external/jlink_monitor_mode_debug/gcc/JLINK_MONITOR_ISR_SES.s
endif

INC_DIRS += \
	$(SDK_ROOT)/components/libraries/log \
	$(SDK_ROOT)/components/libraries/fstorage \
	$(SDK_ROOT)/components/drivers_nrf/gpiote \
	$(SDK_ROOT)/components/libraries/fifo \
	$(SDK_ROOT)/components/drivers_nrf/common \
	$(SDK_ROOT)/components/ble/ble_advertising \
	$(SDK_ROOT)/components/drivers_nrf/uart \
	$(SDK_ROOT)/components/ble/common \
	$(SDK_ROOT)/components/libraries/experimental_section_vars \
	$(SDK_ROOT)/components/softdevice/s132/headers \
	$(SDK_ROOT)/components/drivers_nrf/hal \
	$(SDK_ROOT)/components/drivers_nrf/delay \
	$(SDK_ROOT)/components/toolchain/cmsis/include \
	$(SDK_ROOT)/components/libraries/util \
	../config \
	$(SDK_ROOT)/components/libraries/uart \
	$(SDK_ROOT)/components/libraries/timer \
	$(SDK_ROOT)/components/toolchain \
	$(SDK_ROOT)/components/ble/ble_services/ble_nus \
	$(SDK_ROOT)/components/device \
	$(SDK_ROOT)/components/libraries/button \
	$(SDK_ROOT)/components/drivers_nrf/clock \
	$(SDK_ROOT)/components/softdevice/common/softdevice_handler \
	$(SDK_ROOT)/components/libraries/log/src \
	$(SDK_ROOT)/components/ble/nrf_ble_gatt \
	$(SDK_ROOT)/components/libraries/strerror \
	$(SDK_ROOT)/components/libraries/bsp \
	$(SDK_ROOT)/components/boards \
	$(SDK_ROOT)/external/segger_rtt
ifdef MMD
	INC_DIRS += $(SDK_ROOT)/external/jlink_monitor_mode_debug/gcc
endif

# Convert to absolute paths and sort to remove duplicates.
SRC_FILES := $(sort $(foreach f,$(SRC_FILES),$(abspath $(f))))
INC_DIRS := $(sort $(foreach d,$(INC_DIRS),$(abspath $(d))))

SRC_DIRS := $(dir $(SRC_FILES) $(ASM_FILES))

SRC_FILE_NAMES := $(notdir $(SRC_FILES) $(ASM_FILES))

# Convert each source file name into the form '$(OBJ_DIR)/$(SRC_FILE).o'.
OBJ := $(patsubst %,%.o,$(basename $(SRC_FILE_NAMES)))
DBG_OBJ := $(addprefix $(DBG_BUILD_DIR)/,$(OBJ))
REL_OBJ := $(addprefix $(REL_BUILD_DIR)/,$(OBJ))

.PHONY: default
default: CFLAGS += -O0 -ggdb -DDEBUG -DDEBUG_NRF
default: OBJ_DIR := $(DBG_BUILD_DIR)
default: $(DBG_BUILD_DIR)/$(PROJECT_NAME).hex
	$(call echosize,$(DBG_BUILD_DIR)/$(PROJECT_NAME).out)

.PHONY: release
release: CFLAGS += -O3 -g3
release: OBJ_DIR := $(REL_BUILD_DIR)
release: $(REL_BUILD_DIR)/$(PROJECT_NAME).bin $(REL_BUILD_DIR)/$(PROJECT_NAME).hex
	$(call echosize,$(REL_BUILD_DIR)/$(PROJECT_NAME).out)
ifdef MMD
	@echo "Use of the MMD parameter is not recommended for release builds."
endif

.PHONY: all
all: default release

DEPS := $(addprefix $(DEPS_DIR)/,$(OBJ:.o=.d))
-include $(DEPS)

INCLUDES := $(patsubst %,-I%,$(INC_DIRS))

vpath %.c $(SRC_DIRS)
vpath %.s $(SRC_DIRS)

define echosize
	@echo ''
	@'$(SIZE)' $1;
	@echo ''
endef

define flash
	@"$(NRFJPROG)" $(NRFJPROG_SN) --program $1 -f nrf52 --sectorerase --verify
	@"$(NRFJPROG)" $(NRFJPROG_SN) --reset -f nrf52
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
	@echo "target remote localhost:$(GDB_PORT)" > $(GDB_CMD_PATH)
	@echo "mon speed 10000" >> $(GDB_CMD_PATH)
	@echo "mon flash download=1" >> $(GDB_CMD_PATH)
	@echo "load $(ELF_PATH)" >> $(GDB_CMD_PATH)
ifdef MMD
	@echo "mon exec SetMonModeDebug=1" >> $(GDB_CMD_PATH)
	@echo "mon exec SetMonModeVTableAddr=$(APP_FLASH_LOCATION)" >> $(GDB_CMD_PATH)
endif
	@echo "break main" >> $(GDB_CMD_PATH)
	@echo "mon reset 0" >> $(GDB_CMD_PATH)
	@$(TERMINAL) "'$(GDBSERVER)' $(GDB_SERVER_SN) -device nrf52832_XXAA \
		-if swd -port $(GDB_PORT)" $(BG_JOB)
	@$(TERMINAL) "'$(GDB)' $(ELF_PATH) -x $(GDB_CMD_PATH)"

.PHONY: gdb_rtt
gdb_rtt: gdb
	@$(TERMINAL) "'$(RTT_CLIENT)'"

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
	@echo "    gdb_rtt [SN=1234]      - Call gdb target and then open RTT Client"
	@echo "    flash_sd [SN=1234]     - Flash the SoftDevice"
	@echo "    flash_debug [SN=1234]  - Flash the debug build"
	@echo "    flash_release [SN=1234]- Flash the release build"
	@echo "The following params are available:"
	@echo "    MMD=1                  - Enable Monitor Mode Debugging"

# This is a special target that tells make to delete a file if an error occurs
# while the file is being generated.
.DELETE_ON_ERROR:
