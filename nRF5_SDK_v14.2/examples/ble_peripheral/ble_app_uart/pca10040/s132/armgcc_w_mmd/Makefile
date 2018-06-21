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

SD_HEX_PATH := $(SDK_ROOT)/components/softdevice/s132/hex/s132_nrf52_5.0.0_softdevice.hex

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
CC := $(GNU_INSTALL_ROOT)/$(GNU_PREFIX)-gcc
AS := $(GNU_INSTALL_ROOT)/$(GNU_PREFIX)-as
AR := $(GNU_INSTALL_ROOT)/$(GNU_PREFIX)-ar -r
LD := $(GNU_INSTALL_ROOT)/$(GNU_PREFIX)-ld
NM := $(GNU_INSTALL_ROOT)/$(GNU_PREFIX)-nm
OBJDUMP := $(GNU_INSTALL_ROOT)/$(GNU_PREFIX)-objdump
OBJCOPY := $(GNU_INSTALL_ROOT)/$(GNU_PREFIX)-objcopy
SIZE := $(GNU_INSTALL_ROOT)/$(GNU_PREFIX)-size
GDB := $(GNU_INSTALL_ROOT)/$(GNU_PREFIX)-gdb

SHAREDFLAGS += \
	-DNRF52 \
	-DNRF52832_XXAA \
	-DCONFIG_GPIO_AS_PINRESET \
	-DSWI_DISABLE0 \
	-DFLOAT_ABI_HARD \
	-DBOARD_$(BOARD) \
	-DS132 \
	-DSOFTDEVICE_PRESENT \
	-DNRF_SD_BLE_API_VERSION=5 \
	-DNRF52_PAN_74

CFLAGS += \
	-mcpu=cortex-m4 \
	-mthumb \
	--std=gnu99 \
	-Wall \
	-Werror \
	-mfloat-abi=hard \
	-mfpu=fpv4-sp-d16 \
	-ffunction-sections \
	-fdata-sections \
	-fno-strict-aliasing \
	-fno-builtin \
	-fshort-enums \
	-mabi=aapcs \
	$(SHAREDFLAGS) \
ifdef MMD
	CFLAGS += -DMMD
endif

ASMFLAGS += \
	-mcpu=cortex-m4 \
	-x assembler-with-cpp \
	-mfloat-abi=hard \
	-mfpu=fpv4-sp-d16 \
	-mabi=aapcs \
	-mthumb \
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

# Add standard libraries at the very end of the linker input, after all objects
# that may need symbols provided by these libraries.
LIB_FILES += \
	-lc \
	-lnosys \
	-lm

SRC_FILES += \
	$(SDK_ROOT)/components/libraries/experimental_log/src/nrf_log_backend_rtt.c \
	$(SDK_ROOT)/components/libraries/experimental_log/src/nrf_log_backend_serial.c \
	$(SDK_ROOT)/components/libraries/experimental_log/src/nrf_log_default_backends.c \
	$(SDK_ROOT)/components/libraries/experimental_log/src/nrf_log_frontend.c \
	$(SDK_ROOT)/components/libraries/experimental_log/src/nrf_log_str_formatter.c \
	$(SDK_ROOT)/components/libraries/button/app_button.c \
	$(SDK_ROOT)/components/libraries/util/app_error.c \
	$(SDK_ROOT)/components/libraries/util/app_error_weak.c \
	$(SDK_ROOT)/components/libraries/fifo/app_fifo.c \
	$(SDK_ROOT)/components/libraries/scheduler/app_scheduler.c \
	$(SDK_ROOT)/components/libraries/timer/app_timer.c \
	$(SDK_ROOT)/components/libraries/uart/app_uart_fifo.c \
	$(SDK_ROOT)/components/libraries/util/app_util_platform.c \
	$(SDK_ROOT)/components/libraries/hardfault/hardfault_implementation.c \
	$(SDK_ROOT)/components/libraries/util/nrf_assert.c \
	$(SDK_ROOT)/components/libraries/atomic_fifo/nrf_atfifo.c \
	$(SDK_ROOT)/components/libraries/balloc/nrf_balloc.c \
	$(SDK_ROOT)/external/fprintf/nrf_fprintf.c \
	$(SDK_ROOT)/external/fprintf/nrf_fprintf_format.c \
	$(SDK_ROOT)/components/libraries/fstorage/nrf_fstorage.c \
	$(SDK_ROOT)/components/libraries/fstorage/nrf_fstorage_sd.c \
	$(SDK_ROOT)/components/libraries/experimental_memobj/nrf_memobj.c \
	$(SDK_ROOT)/components/libraries/pwr_mgmt/nrf_pwr_mgmt.c \
	$(SDK_ROOT)/components/libraries/experimental_section_vars/nrf_section_iter.c \
	$(SDK_ROOT)/components/libraries/strerror/nrf_strerror.c \
	$(SDK_ROOT)/components/libraries/uart/retarget.c \
	$(SDK_ROOT)/components/libraries/util/sdk_mapped_flags.c \
	$(SDK_ROOT)/components/boards/boards.c \
	$(SDK_ROOT)/components/drivers_nrf/clock/nrf_drv_clock.c \
	$(SDK_ROOT)/components/drivers_nrf/common/nrf_drv_common.c \
	$(SDK_ROOT)/components/drivers_nrf/gpiote/nrf_drv_gpiote.c \
	$(SDK_ROOT)/components/drivers_nrf/uart/nrf_drv_uart.c \
	$(SDK_ROOT)/components/libraries/bsp/bsp.c \
	$(SDK_ROOT)/components/libraries/bsp/bsp_btn_ble.c \
	$(SDK_ROOT)/components/libraries/bsp/bsp_nfc.c \
	$(PROJ_DIR)/main.c \
	$(SDK_ROOT)/external/segger_rtt/SEGGER_RTT.c \
	$(SDK_ROOT)/external/segger_rtt/SEGGER_RTT_Syscalls_GCC.c \
	$(SDK_ROOT)/external/segger_rtt/SEGGER_RTT_printf.c \
	$(SDK_ROOT)/components/ble/common/ble_advdata.c \
	$(SDK_ROOT)/components/ble/ble_advertising/ble_advertising.c \
	$(SDK_ROOT)/components/ble/common/ble_conn_params.c \
	$(SDK_ROOT)/components/ble/common/ble_conn_state.c \
	$(SDK_ROOT)/components/ble/common/ble_srv_common.c \
	$(SDK_ROOT)/components/ble/nrf_ble_gatt/nrf_ble_gatt.c \
	$(SDK_ROOT)/components/toolchain/system_nrf52.c \
	$(SDK_ROOT)/components/ble/ble_services/ble_nus/ble_nus.c \
	$(SDK_ROOT)/components/softdevice/common/nrf_sdh.c \
	$(SDK_ROOT)/components/softdevice/common/nrf_sdh_ble.c \
	$(SDK_ROOT)/components/softdevice/common/nrf_sdh_soc.c \
ifdef MMD
	SRC_FILES += $(SDK_ROOT)/external/jlink_monitor_mode_debug/gcc/JLINK_MONITOR.c
endif

ASM_FILES += \
	$(SDK_ROOT)/components/toolchain/gcc/gcc_startup_nrf52.s
ifdef MMD
	ASM_FILES += $(SDK_ROOT)/external/jlink_monitor_mode_debug/gcc/JLINK_MONITOR_ISR_SES.s
endif

INC_DIRS += \
	$(SDK_ROOT)/components/drivers_nrf/comp \
	$(SDK_ROOT)/components/drivers_nrf/twi_master \
	$(SDK_ROOT)/components/ble/ble_services/ble_ancs_c \
	$(SDK_ROOT)/components/ble/ble_services/ble_ias_c \
	$(SDK_ROOT)/components/libraries/pwm \
	$(SDK_ROOT)/components/softdevice/s132/headers/nrf52 \
	$(SDK_ROOT)/components/libraries/usbd/class/cdc/acm \
	$(SDK_ROOT)/components/libraries/usbd/class/hid/generic \
	$(SDK_ROOT)/components/libraries/usbd/class/msc \
	$(SDK_ROOT)/components/libraries/usbd/class/hid \
	$(SDK_ROOT)/components/libraries/experimental_log \
	$(SDK_ROOT)/components/ble/ble_services/ble_gls \
	$(SDK_ROOT)/components/libraries/fstorage \
	$(SDK_ROOT)/components/drivers_nrf/i2s \
	$(SDK_ROOT)/components/libraries/mutex \
	$(SDK_ROOT)/components/libraries/gpiote \
	$(SDK_ROOT)/components/libraries/experimental_log/src \
	$(SDK_ROOT)/components/drivers_nrf/gpiote \
	$(SDK_ROOT)/components/libraries/fifo \
	$(SDK_ROOT)/components/boards \
	$(SDK_ROOT)/components/libraries/experimental_memobj \
	$(SDK_ROOT)/components/drivers_nrf/common \
	$(SDK_ROOT)/components/ble/ble_advertising \
	$(SDK_ROOT)/components/ble/ble_services/ble_bas_c \
	$(SDK_ROOT)/components/ble/ble_services/ble_hrs_c \
	$(SDK_ROOT)/components/libraries/queue \
	$(SDK_ROOT)/components/libraries/pwr_mgmt \
	$(SDK_ROOT)/components/ble/ble_dtm \
	$(SDK_ROOT)/components/toolchain/cmsis/include \
	$(SDK_ROOT)/components/ble/ble_services/ble_rscs_c \
	$(SDK_ROOT)/components/drivers_nrf/uart \
	$(SDK_ROOT)/components/ble/common \
	$(SDK_ROOT)/components/ble/ble_services/ble_lls \
	$(SDK_ROOT)/components/drivers_nrf/wdt \
	$(SDK_ROOT)/components/libraries/bsp \
	$(SDK_ROOT)/components/ble/ble_services/ble_bas \
	$(SDK_ROOT)/components/libraries/experimental_section_vars \
	$(SDK_ROOT)/components/softdevice/s132/headers \
	$(SDK_ROOT)/components/ble/ble_services/ble_ans_c \
	$(SDK_ROOT)/components/libraries/slip \
	$(SDK_ROOT)/components/libraries/mem_manager \
	$(SDK_ROOT)/external/segger_rtt \
	$(SDK_ROOT)/components/libraries/usbd/class/cdc \
	$(SDK_ROOT)/components/drivers_nrf/hal \
	$(SDK_ROOT)/components/ble/ble_services/ble_nus_c \
	$(SDK_ROOT)/components/drivers_nrf/rtc \
	$(SDK_ROOT)/components/softdevice/common \
	$(SDK_ROOT)/components/ble/ble_services/ble_ias \
	$(SDK_ROOT)/components/libraries/usbd/class/hid/mouse \
	$(SDK_ROOT)/components/libraries/ecc \
	$(SDK_ROOT)/components/drivers_nrf/ppi \
	$(SDK_ROOT)/components/ble/ble_services/ble_dfu \
	$(SDK_ROOT)/external/fprintf \
	$(SDK_ROOT)/components/drivers_nrf/twis_slave \
	$(SDK_ROOT)/components/libraries/atomic \
	$(SDK_ROOT)/components \
	$(SDK_ROOT)/components/libraries/scheduler \
	$(SDK_ROOT)/components/libraries/cli \
	$(SDK_ROOT)/components/ble/ble_services/ble_lbs \
	$(SDK_ROOT)/components/ble/ble_services/ble_hts \
	$(SDK_ROOT)/components/drivers_nrf/delay \
	$(SDK_ROOT)/components/libraries/crc16 \
	$(SDK_ROOT)/components/drivers_nrf/timer \
	$(SDK_ROOT)/components/libraries/util \
	$(SDK_ROOT)/components/drivers_nrf/pwm \
	../config \
	$(SDK_ROOT)/components/libraries/csense_drv \
	$(SDK_ROOT)/components/libraries/csense \
	$(SDK_ROOT)/components/libraries/balloc \
	$(SDK_ROOT)/components/libraries/low_power_pwm \
	$(SDK_ROOT)/components/libraries/hardfault \
	$(SDK_ROOT)/components/ble/ble_services/ble_cscs \
	$(SDK_ROOT)/components/libraries/uart \
	$(SDK_ROOT)/components/libraries/hci \
	$(SDK_ROOT)/components/libraries/usbd/class/hid/kbd \
	$(SDK_ROOT)/components/drivers_nrf/spi_slave \
	$(SDK_ROOT)/components/drivers_nrf/lpcomp \
	$(SDK_ROOT)/components/libraries/timer \
	$(SDK_ROOT)/components/drivers_nrf/rng \
	$(SDK_ROOT)/components/drivers_nrf/power \
	$(SDK_ROOT)/components/libraries/usbd/config \
	$(SDK_ROOT)/components/toolchain \
	$(SDK_ROOT)/components/libraries/led_softblink \
	$(SDK_ROOT)/components/drivers_nrf/qdec \
	$(SDK_ROOT)/components/ble/ble_services/ble_cts_c \
	$(SDK_ROOT)/components/drivers_nrf/spi_master \
	$(SDK_ROOT)/components/ble/ble_services/ble_nus \
	$(SDK_ROOT)/components/libraries/twi_mngr \
	$(SDK_ROOT)/components/ble/ble_services/ble_hids \
	$(SDK_ROOT)/components/libraries/strerror \
	$(SDK_ROOT)/components/drivers_nrf/pdm \
	$(SDK_ROOT)/components/libraries/crc32 \
	$(SDK_ROOT)/components/libraries/usbd/class/audio \
	$(SDK_ROOT)/components/ble/peer_manager \
	$(SDK_ROOT)/components/drivers_nrf/swi \
	$(SDK_ROOT)/components/ble/ble_services/ble_tps \
	$(SDK_ROOT)/components/ble/ble_services/ble_dis \
	$(SDK_ROOT)/components/device \
	$(SDK_ROOT)/components/ble/nrf_ble_gatt \
	$(SDK_ROOT)/components/ble/nrf_ble_qwr \
	$(SDK_ROOT)/components/libraries/button \
	$(SDK_ROOT)/components/libraries/usbd \
	$(SDK_ROOT)/components/drivers_nrf/saadc \
	$(SDK_ROOT)/components/libraries/atomic_fifo \
	$(SDK_ROOT)/components/ble/ble_services/ble_lbs_c \
	$(SDK_ROOT)/components/ble/ble_racp \
	$(SDK_ROOT)/components/toolchain/gcc \
	$(SDK_ROOT)/components/libraries/fds \
	$(SDK_ROOT)/components/libraries/twi \
	$(SDK_ROOT)/components/drivers_nrf/clock \
	$(SDK_ROOT)/components/ble/ble_services/ble_rscs \
	$(SDK_ROOT)/components/drivers_nrf/usbd \
	$(SDK_ROOT)/components/ble/ble_services/ble_hrs
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
default: CFLAGS += -O0 -ggdb
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
	@echo Assembling file: $(notdir $<)
	@'$(CC)' $(ASMFLAGS) $(INCLUDES) -c -o $@ $<

$(DBG_BUILD_DIR)/$(PROJECT_NAME).hex: $(DBG_BUILD_DIR)/$(PROJECT_NAME).out
	@echo Creating hex file: $(notdir $@)
	@'$(OBJCOPY)' -O ihex $(DBG_BUILD_DIR)/$(PROJECT_NAME).out $@

$(DBG_BUILD_DIR)/$(PROJECT_NAME).bin: $(DBG_BUILD_DIR)/$(PROJECT_NAME).out
	@echo Creating bin file: $(notdir $@)
	@'$(OBJCOPY)' -O binary $(DBG_BUILD_DIR)/$(PROJECT_NAME).out $@

$(DBG_BUILD_DIR)/$(PROJECT_NAME).out: $(DBG_OBJ)
	@echo Linking ELF file: $(notdir $@)
	@'$(CC)' $(LDFLAGS) $(DBG_OBJ) $(LIB_FILES) -o $@

$(REL_BUILD_DIR)/%.o: %.c | $(REL_BUILD_DIR)
	@echo Compiling file: $(notdir $<)
	@'$(CC)' $(CFLAGS) $(INCLUDES) -c -o $@ $<

$(REL_BUILD_DIR)/%.o: %.s | $(REL_BUILD_DIR)
	@echo Assembling file: $(notdir $<)
	@'$(CC)' $(ASMFLAGS) $(INCLUDES) -c -o $@ $<

$(REL_BUILD_DIR)/$(PROJECT_NAME).hex: $(REL_BUILD_DIR)/$(PROJECT_NAME).out
	@echo Creating hex file: $(notdir $@)
	@'$(OBJCOPY)' -O ihex $(REL_BUILD_DIR)/$(PROJECT_NAME).out $@

$(REL_BUILD_DIR)/$(PROJECT_NAME).bin: $(REL_BUILD_DIR)/$(PROJECT_NAME).out
	@echo Creating bin file: $(notdir $@)
	@'$(OBJCOPY)' -O binary $(REL_BUILD_DIR)/$(PROJECT_NAME).out $@

$(REL_BUILD_DIR)/$(PROJECT_NAME).out: $(REL_OBJ)
	@echo Linking ELF file: $(notdir $@)
	@'$(CC)' $(LDFLAGS) $(REL_OBJ) $(LIB_FILES) -o $@

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
	@$(TERMINAL) "'$(GDBSERVER)' $(GDB_SERVER_SN) -device nrf52 \
		-if swd -port $(GDB_PORT)" $(BG_JOB)
	@echo "target remote localhost:$(GDB_PORT)" > $(GDB_CMD_PATH)
	@echo "break main" >> $(GDB_CMD_PATH)
	@echo "mon speed 10000" >> $(GDB_CMD_PATH)
	@echo "mon flash download= 1" >> $(GDB_CMD_PATH)
	@echo "load $(ELF_PATH)" >> $(GDB_CMD_PATH)
ifdef MMD
	@echo "mon exec SetMonModeDebug=1" >> $(GDB_CMD_PATH)
	@echo "mon exec SetMonModeVTableAddr=$(APP_FLASH_LOCATION)" >> $(GDB_CMD_PATH)
endif
	@echo "mon reset 0" >> $(GDB_CMD_PATH)
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
