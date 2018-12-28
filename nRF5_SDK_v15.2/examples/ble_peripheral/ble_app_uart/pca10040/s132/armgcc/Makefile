# The PROJECT_NAME can be changed arbitrarily (it does not depend on anything).
PROJECT_NAME := ble_app_uart_pca10040_s132

# The LINKER_SCRIPT is usually in the same directory as the Makefile.
LINKER_SCRIPT := ble_app_uart_gcc_nrf52.ld

BOARD := PCA10040

DBG_BUILD_DIR := ./_debug
REL_BUILD_DIR := ./_release
DEPS_DIR := ./_deps

SDK_ROOT := ../../../../../..
PROJ_DIR := ../../..

# JLINK_MON_DEBUG_DIR should point to the directory that contains the files
# in JLINK_MON_DEBUG_FILES plus JLINK_MONITOR.h. If Monitor Mode Debugging is
# not required then leave JLINK_MON_DEBUG_DIR empty.
JLINK_MON_DEBUG_DIR := 

# The offset of the application needs to be specified so the J-Link knows
# the location of the DebugMon_Handler. For the S132 v5 this is 0x23000.
JLINK_MON_DEBUG_APP_FLASH_LOCATION := 0x23000

# If the JLINK_MON_DEBUG_DIR is empty then make sure it is evaluated correctly.
JLINK_MON_DEBUG_DIR := $(strip $(JLINK_MON_DEBUG_DIR))

# These are the required files as of version 6.12a of the J-Link driver.
JLINK_MON_DEBUG_FILES := JLINK_MONITOR.c JLINK_MONITOR_ISR_SES.s

# Init commands will be written to a file and then specified when starting GDB
# instead of relying on .gdbinit (to avoid having to enable .gbdinit files).
GDB_CMD_PATH := $(DBG_BUILD_DIR)/gdb.txt

SD_HEX_PATH := $(SDK_ROOT)/components/softdevice/s132/hex/s132_nrf52_6.1.0_softdevice.hex

# Include the correct template Makefile depending on platform.
TEMPLATE_PATH = $(SDK_ROOT)/components/toolchain/gcc
ifeq ($(OS),Windows_NT)
	include $(TEMPLATE_PATH)/Makefile.windows
# The Windows command shell 'start' function is used so the executable
# is started in its own window.
	TERMINAL := cmd /c start ""
	TERMINAL_END := 
	NRFJPROG := nrfjprog.exe
	GDBSERVER := JLinkGDBServerCL.exe
	RTT_CLIENT := JLinkRTTClient.exe
else
	include $(TEMPLATE_PATH)/Makefile.posix
	TERMINAL := gnome-terminal -e "
	TERMINAL_END := "
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
	-DNRF_SD_BLE_API_VERSION=6 \
	-DNRF52_PAN_74 \
	-D__HEAP_SIZE=8192 \
	-D__STACK_SIZE=8192

CFLAGS += \
	-mcpu=cortex-m4 \
	-mthumb \
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
	$(SHAREDFLAGS)

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
	-L$(SDK_ROOT)/modules/nrfx/mdk \
	-T$(LINKER_SCRIPT) \
	-mcpu=cortex-m4 \
	-mfloat-abi=hard \
	-mfpu=fpv4-sp-d16 \
	-Wl,--gc-sections \
	--specs=nano.specs

# Add standard libraries at the very end of the linker input, after all objects
# that may need symbols provided by these libraries.
LIB_FILES += \
	-lc \
	-lnosys \
	-lm

SRC_FILES += \
	$(SDK_ROOT)/modules/nrfx/mdk/gcc_startup_nrf52.S \
	$(SDK_ROOT)/components/libraries/log/src/nrf_log_backend_rtt.c \
	$(SDK_ROOT)/components/libraries/log/src/nrf_log_backend_serial.c \
	$(SDK_ROOT)/components/libraries/log/src/nrf_log_default_backends.c \
	$(SDK_ROOT)/components/libraries/log/src/nrf_log_frontend.c \
	$(SDK_ROOT)/components/libraries/log/src/nrf_log_str_formatter.c \
	$(SDK_ROOT)/components/libraries/button/app_button.c \
	$(SDK_ROOT)/components/libraries/util/app_error.c \
	$(SDK_ROOT)/components/libraries/util/app_error_handler_gcc.c \
	$(SDK_ROOT)/components/libraries/util/app_error_weak.c \
	$(SDK_ROOT)/components/libraries/fifo/app_fifo.c \
	$(SDK_ROOT)/components/libraries/scheduler/app_scheduler.c \
	$(SDK_ROOT)/components/libraries/timer/app_timer.c \
	$(SDK_ROOT)/components/libraries/uart/app_uart_fifo.c \
	$(SDK_ROOT)/components/libraries/util/app_util_platform.c \
	$(SDK_ROOT)/components/libraries/hardfault/hardfault_implementation.c \
	$(SDK_ROOT)/components/libraries/util/nrf_assert.c \
	$(SDK_ROOT)/components/libraries/atomic_fifo/nrf_atfifo.c \
	$(SDK_ROOT)/components/libraries/atomic_flags/nrf_atflags.c \
	$(SDK_ROOT)/components/libraries/atomic/nrf_atomic.c \
	$(SDK_ROOT)/components/libraries/balloc/nrf_balloc.c \
	$(SDK_ROOT)/external/fprintf/nrf_fprintf.c \
	$(SDK_ROOT)/external/fprintf/nrf_fprintf_format.c \
	$(SDK_ROOT)/components/libraries/memobj/nrf_memobj.c \
	$(SDK_ROOT)/components/libraries/pwr_mgmt/nrf_pwr_mgmt.c \
	$(SDK_ROOT)/components/libraries/ringbuf/nrf_ringbuf.c \
	$(SDK_ROOT)/components/libraries/experimental_section_vars/nrf_section_iter.c \
	$(SDK_ROOT)/components/libraries/strerror/nrf_strerror.c \
	$(SDK_ROOT)/components/libraries/uart/retarget.c \
	$(SDK_ROOT)/modules/nrfx/mdk/system_nrf52.c \
	$(SDK_ROOT)/components/boards/boards.c \
	$(SDK_ROOT)/integration/nrfx/legacy/nrf_drv_clock.c \
	$(SDK_ROOT)/integration/nrfx/legacy/nrf_drv_uart.c \
	$(SDK_ROOT)/modules/nrfx/drivers/src/nrfx_clock.c \
	$(SDK_ROOT)/modules/nrfx/drivers/src/nrfx_gpiote.c \
	$(SDK_ROOT)/modules/nrfx/drivers/src/nrfx_power_clock.c \
	$(SDK_ROOT)/modules/nrfx/drivers/src/prs/nrfx_prs.c \
	$(SDK_ROOT)/modules/nrfx/drivers/src/nrfx_uart.c \
	$(SDK_ROOT)/modules/nrfx/drivers/src/nrfx_uarte.c \
	$(SDK_ROOT)/components/libraries/bsp/bsp.c \
	$(SDK_ROOT)/components/libraries/bsp/bsp_btn_ble.c \
	$(PROJ_DIR)/main.c \
	$(SDK_ROOT)/external/segger_rtt/SEGGER_RTT.c \
	$(SDK_ROOT)/external/segger_rtt/SEGGER_RTT_Syscalls_GCC.c \
	$(SDK_ROOT)/external/segger_rtt/SEGGER_RTT_printf.c \
	$(SDK_ROOT)/components/ble/common/ble_advdata.c \
	$(SDK_ROOT)/components/ble/ble_advertising/ble_advertising.c \
	$(SDK_ROOT)/components/ble/common/ble_conn_params.c \
	$(SDK_ROOT)/components/ble/common/ble_conn_state.c \
	$(SDK_ROOT)/components/ble/ble_link_ctx_manager/ble_link_ctx_manager.c \
	$(SDK_ROOT)/components/ble/common/ble_srv_common.c \
	$(SDK_ROOT)/components/ble/nrf_ble_gatt/nrf_ble_gatt.c \
	$(SDK_ROOT)/components/ble/nrf_ble_qwr/nrf_ble_qwr.c \
	$(SDK_ROOT)/external/utf_converter/utf.c \
	$(SDK_ROOT)/components/ble/ble_services/ble_nus/ble_nus.c \
	$(SDK_ROOT)/components/softdevice/common/nrf_sdh.c \
	$(SDK_ROOT)/components/softdevice/common/nrf_sdh_ble.c \
	$(SDK_ROOT)/components/softdevice/common/nrf_sdh_soc.c

INC_DIRS += \
	$(SDK_ROOT)/components/nfc/ndef/generic/message \
	$(SDK_ROOT)/components/nfc/t2t_lib \
	$(SDK_ROOT)/components/nfc/t4t_parser/hl_detection_procedure \
	$(SDK_ROOT)/components/ble/ble_services/ble_ancs_c \
	$(SDK_ROOT)/components/ble/ble_services/ble_ias_c \
	$(SDK_ROOT)/components/libraries/pwm \
	$(SDK_ROOT)/components/softdevice/s132/headers/nrf52 \
	$(SDK_ROOT)/components/libraries/usbd/class/cdc/acm \
	$(SDK_ROOT)/components/libraries/usbd/class/hid/generic \
	$(SDK_ROOT)/components/libraries/usbd/class/msc \
	$(SDK_ROOT)/components/libraries/usbd/class/hid \
	$(SDK_ROOT)/modules/nrfx/hal \
	$(SDK_ROOT)/components/nfc/ndef/conn_hand_parser/le_oob_rec_parser \
	$(SDK_ROOT)/components/libraries/log \
	$(SDK_ROOT)/components/ble/ble_services/ble_gls \
	$(SDK_ROOT)/components/libraries/fstorage \
	$(SDK_ROOT)/components/nfc/ndef/text \
	$(SDK_ROOT)/components/libraries/mutex \
	$(SDK_ROOT)/components/libraries/gfx \
	$(SDK_ROOT)/components/libraries/bootloader/ble_dfu \
	$(SDK_ROOT)/components/nfc/ndef/connection_handover/common \
	$(SDK_ROOT)/components/libraries/fifo \
	$(SDK_ROOT)/components/boards \
	$(SDK_ROOT)/components/nfc/ndef/generic/record \
	$(SDK_ROOT)/components/nfc/t4t_parser/cc_file \
	$(SDK_ROOT)/components/ble/ble_advertising \
	$(SDK_ROOT)/external/utf_converter \
	$(SDK_ROOT)/components/ble/ble_services/ble_bas_c \
	$(SDK_ROOT)/modules/nrfx/drivers/include \
	$(SDK_ROOT)/components/libraries/experimental_task_manager \
	$(SDK_ROOT)/components/ble/ble_services/ble_hrs_c \
	$(SDK_ROOT)/components/nfc/ndef/connection_handover/le_oob_rec \
	$(SDK_ROOT)/components/libraries/queue \
	$(SDK_ROOT)/components/libraries/pwr_mgmt \
	$(SDK_ROOT)/components/ble/ble_dtm \
	$(SDK_ROOT)/components/toolchain/cmsis/include \
	$(SDK_ROOT)/components/ble/ble_services/ble_rscs_c \
	$(SDK_ROOT)/components/ble/common \
	$(SDK_ROOT)/components/ble/ble_services/ble_lls \
	$(SDK_ROOT)/components/libraries/bsp \
	$(SDK_ROOT)/components/nfc/ndef/connection_handover/ac_rec \
	$(SDK_ROOT)/components/ble/ble_services/ble_bas \
	$(SDK_ROOT)/components/libraries/mpu \
	$(SDK_ROOT)/components/libraries/experimental_section_vars \
	$(SDK_ROOT)/components/softdevice/s132/headers \
	$(SDK_ROOT)/components/ble/ble_services/ble_ans_c \
	$(SDK_ROOT)/components/libraries/slip \
	$(SDK_ROOT)/components/libraries/delay \
	$(SDK_ROOT)/components/libraries/mem_manager \
	$(SDK_ROOT)/components/libraries/csense_drv \
	$(SDK_ROOT)/components/libraries/memobj \
	$(SDK_ROOT)/components/ble/ble_services/ble_nus_c \
	$(SDK_ROOT)/components/softdevice/common \
	$(SDK_ROOT)/components/ble/ble_services/ble_ias \
	$(SDK_ROOT)/components/libraries/usbd/class/hid/mouse \
	$(SDK_ROOT)/components/libraries/low_power_pwm \
	$(SDK_ROOT)/components/nfc/ndef/conn_hand_parser/ble_oob_advdata_parser \
	$(SDK_ROOT)/components/ble/ble_services/ble_dfu \
	$(SDK_ROOT)/external/fprintf \
	$(SDK_ROOT)/components/libraries/svc \
	$(SDK_ROOT)/components/libraries/atomic \
	$(SDK_ROOT)/components \
	$(SDK_ROOT)/components/libraries/scheduler \
	$(SDK_ROOT)/components/libraries/cli \
	$(SDK_ROOT)/components/ble/ble_services/ble_lbs \
	$(SDK_ROOT)/components/ble/ble_services/ble_hts \
	$(SDK_ROOT)/components/ble/ble_services/ble_cts_c \
	$(SDK_ROOT)/components/libraries/crc16 \
	$(SDK_ROOT)/components/nfc/t4t_parser/apdu \
	$(SDK_ROOT)/components/libraries/util \
	../config \
	$(SDK_ROOT)/components/libraries/usbd/class/cdc \
	$(SDK_ROOT)/components/libraries/csense \
	$(SDK_ROOT)/components/libraries/balloc \
	$(SDK_ROOT)/components/libraries/ecc \
	$(SDK_ROOT)/components/libraries/hardfault \
	$(SDK_ROOT)/components/ble/ble_services/ble_cscs \
	$(SDK_ROOT)/components/libraries/uart \
	$(SDK_ROOT)/components/libraries/hci \
	$(SDK_ROOT)/components/libraries/usbd/class/hid/kbd \
	$(SDK_ROOT)/components/libraries/timer \
	$(SDK_ROOT)/integration/nrfx \
	$(SDK_ROOT)/components/nfc/t4t_parser/tlv \
	$(SDK_ROOT)/components/libraries/sortlist \
	$(SDK_ROOT)/components/libraries/spi_mngr \
	$(SDK_ROOT)/components/libraries/led_softblink \
	$(SDK_ROOT)/components/nfc/ndef/conn_hand_parser \
	$(SDK_ROOT)/components/libraries/sdcard \
	$(SDK_ROOT)/components/nfc/ndef/parser/record \
	$(SDK_ROOT)/modules/nrfx/mdk \
	$(SDK_ROOT)/components/ble/ble_link_ctx_manager \
	$(SDK_ROOT)/components/ble/ble_services/ble_nus \
	$(SDK_ROOT)/components/libraries/twi_mngr \
	$(SDK_ROOT)/components/ble/ble_services/ble_hids \
	$(SDK_ROOT)/components/libraries/strerror \
	$(SDK_ROOT)/components/libraries/crc32 \
	$(SDK_ROOT)/components/nfc/ndef/connection_handover/ble_oob_advdata \
	$(SDK_ROOT)/components/nfc/t2t_parser \
	$(SDK_ROOT)/components/nfc/ndef/connection_handover/ble_pair_msg \
	$(SDK_ROOT)/components/libraries/usbd/class/audio \
	$(SDK_ROOT)/components/nfc/t4t_lib/hal_t4t \
	$(SDK_ROOT)/components/nfc/t4t_lib \
	$(SDK_ROOT)/components/ble/peer_manager \
	$(SDK_ROOT)/components/drivers_nrf/usbd \
	$(SDK_ROOT)/components/libraries/ringbuf \
	$(SDK_ROOT)/components/ble/ble_services/ble_tps \
	$(SDK_ROOT)/components/nfc/ndef/parser/message \
	$(SDK_ROOT)/components/ble/ble_services/ble_dis \
	$(SDK_ROOT)/components/nfc/ndef/uri \
	$(SDK_ROOT)/components/ble/nrf_ble_gatt \
	$(SDK_ROOT)/components/ble/nrf_ble_qwr \
	$(SDK_ROOT)/components/libraries/gpiote \
	$(SDK_ROOT)/components/libraries/button \
	$(SDK_ROOT)/modules/nrfx \
	$(SDK_ROOT)/components/libraries/twi_sensor \
	$(SDK_ROOT)/integration/nrfx/legacy \
	$(SDK_ROOT)/components/libraries/usbd \
	$(SDK_ROOT)/components/nfc/ndef/connection_handover/ep_oob_rec \
	$(SDK_ROOT)/external/segger_rtt \
	$(SDK_ROOT)/components/libraries/atomic_fifo \
	$(SDK_ROOT)/components/ble/ble_services/ble_lbs_c \
	$(SDK_ROOT)/components/nfc/ndef/connection_handover/ble_pair_lib \
	$(SDK_ROOT)/components/libraries/crypto \
	$(SDK_ROOT)/components/ble/ble_racp \
	$(SDK_ROOT)/components/libraries/fds \
	$(SDK_ROOT)/components/nfc/ndef/launchapp \
	$(SDK_ROOT)/components/libraries/atomic_flags \
	$(SDK_ROOT)/components/ble/ble_services/ble_hrs \
	$(SDK_ROOT)/components/ble/ble_services/ble_rscs \
	$(SDK_ROOT)/components/nfc/ndef/connection_handover/hs_rec \
	$(SDK_ROOT)/components/nfc/t2t_lib/hal_t2t \
	$(SDK_ROOT)/components/nfc/ndef/conn_hand_parser/ac_rec_parser \
	$(SDK_ROOT)/components/libraries/stack_guard \
	$(SDK_ROOT)/components/libraries/log/src

# The Monitor Mode debugging files will always be tracked by make if they are
# used during debugging. They won't be passed to the linker for the release
# version of the build.
DBG_SRC_FILES :=
ifneq "$(JLINK_MON_DEBUG_DIR)" ""
	INC_DIRS += $(JLINK_MON_DEBUG_DIR)
	DBG_SRC_FILES += $(addprefix $(JLINK_MON_DEBUG_DIR)/, $(JLINK_MON_DEBUG_FILES))
else
$(warning Define JLINK_MON_DEBUG_DIR to enable Monitor Mode Debugging.)
endif

ASSEMBLY_EXTS := s S

# Convert to absolute paths and sort to remove duplicates.
SRC_FILES := $(sort $(foreach f,$(SRC_FILES),$(abspath $(f))))
DBG_SRC_FILES := $(sort $(foreach f,$(DBG_SRC_FILES),$(abspath $(f))))
INC_DIRS := $(sort $(foreach d,$(INC_DIRS),$(abspath $(d))))

# Split the file paths into file names and directories. And remove duplicates.
SRC_DIRS := $(sort $(dir $(SRC_FILES)))
SRC_FILE_NAMES := $(notdir $(SRC_FILES))
DBG_SRC_DIRS := $(sort $(dir $(DBG_SRC_FILES)))
DBG_SRC_FILE_NAMES := $(notdir $(DBG_SRC_FILES))

# Convert each source file name into the form '$(OBJ_DIR)/$(SRC_FILE).o'.
OBJ := $(patsubst %,%.o,$(basename $(SRC_FILE_NAMES)))
DBG_OBJ := $(patsubst %,%.o,$(basename $(DBG_SRC_FILE_NAMES)))
DBG_OBJ := $(addprefix $(DBG_BUILD_DIR)/,$(OBJ) $(DBG_OBJ))
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

.PHONY: all
all: default release

DEPS := $(addprefix $(DEPS_DIR)/,$(OBJ:.o=.d))
-include $(DEPS)

INCLUDES := $(patsubst %,-I%,$(INC_DIRS))

# Look for all source files in SRC_DIRS.
vpath % $(SRC_DIRS) $(DBG_SRC_DIRS)

define echosize
	@echo ''
	@'$(SIZE)' $1
	@echo ''
endef

define flash
	@"$(NRFJPROG)" $(NRFJPROG_SN) --program $1 -f nrf52 --sectorerase --verify
	@"$(NRFJPROG)" $(NRFJPROG_SN) --reset -f nrf52
endef

$(DBG_BUILD_DIR)/%.o: %.c | $(DBG_BUILD_DIR)
	@echo Compiling file: $(notdir $<)
	@'$(CC)' $(CFLAGS) $(INCLUDES) -c -o $@ $<

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
	@printf "$(DBG_BUILD_DIR)/$(notdir $(<:.c=.o)) " >$@
	@"$(CC)" $(CFLAGS) $(INCLUDES) -c $< -MM \
		-MT $(REL_BUILD_DIR)/$(notdir $(<:.c=.o)) >> $@

# The eval command is used to create a different version of these targets for
# each extension in the ASSEMBLY_EXTS list.
define assembly_targets
$$(DBG_BUILD_DIR)/%.o: %.$1 | $$(DBG_BUILD_DIR)
	@echo Compiling assembly file: $$(notdir $$<)
	@'$$(CC)' $$(ASMFLAGS) $$(INCLUDES) -c -o $$@ $$<

$$(REL_BUILD_DIR)/%.o: %.$1 | $$(REL_BUILD_DIR)
	@echo Compiling assembly file: $$(notdir $$<)
	@'$$(CC)' $$(ASMFLAGS) $$(INCLUDES) -c -o $$@ $$<

$$(DEPS_DIR)/%.d: %.$1 | $$(DEPS_DIR)
	@echo Adding dependency for file: $$(notdir $$<)
	@printf "$$(DBG_BUILD_DIR)/$$(notdir $$(<:.$1=.o)) " >$$@
	@"$$(CC)" $$(ASMFLAGS) $$(INCLUDES) -c $$< -MM \
		-MT $$(REL_BUILD_DIR)/$$(notdir $$(<:.$1=.o)) >>$$@
endef
$(foreach EXT,$(ASSEMBLY_EXTS),$(eval $(call assembly_targets,$(EXT))))

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

.PHONY: gdb_cmd_file
gdb_cmd_file: default
	@echo "target remote localhost:$(GDB_PORT)" > $(GDB_CMD_PATH)
	@echo "mon speed 10000" >> $(GDB_CMD_PATH)
	@echo "mon flash download=1" >> $(GDB_CMD_PATH)
	@echo "load $(DBG_BUILD_DIR)/$(PROJECT_NAME).out" >> $(GDB_CMD_PATH)
	@echo "break main" >> $(GDB_CMD_PATH)
	@echo "mon reset 0" >> $(GDB_CMD_PATH)
	@echo "c" >> $(GDB_CMD_PATH)

.PHONY: gdb_mon_cmd_file
gdb_mon_cmd_file: gdb_cmd_file
	@echo "mon exec SetMonModeDebug=1" >> $(GDB_CMD_PATH)
	@echo "mon exec SetMonModeVTableAddr=$(JLINK_MON_DEBUG_APP_FLASH_LOCATION)" >> $(GDB_CMD_PATH)

.PHONY: gdb_cli
gdb_cli:
	@$(TERMINAL) '$(GDBSERVER)' $(GDB_SERVER_SN) -device nrf52832_XXAA \
		-if swd -port $(GDB_PORT) $(TERMINAL_END)
	@$(TERMINAL) '$(GDB)' $(DBG_BUILD_DIR)/$(PROJECT_NAME).out -x $(GDB_CMD_PATH) $(TERMINAL_END)

.PHONY: rtt
rtt:
	@$(TERMINAL) '$(RTT_CLIENT)' $(TERMINAL_END)

.PHONY: gdb
gdb: gdb_cmd_file gdb_cli

.PHONY: gdb_mon
gdb_mon: gdb_mon_cmd_file gdb_cli

.PHONY: gdb_rtt
gdb_rtt: gdb rtt

.PHONY: gdb_mon_rtt
gdb_mon_rtt: gdb_mon rtt

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
ifneq "$(JLINK_MON_DEBUG_DIR)" ""
	@echo "    gdb_mon [SN=1234]      - Enable Monitor Mode Debugging"
	@echo "    gdb_mon_rtt [SN=1234]  - Enable Mon Debugging and open RTT Client"
endif
	@echo "    flash_sd [SN=1234]     - Flash the SoftDevice"
	@echo "    flash_debug [SN=1234]  - Flash the debug build"
	@echo "    flash_release [SN=1234]- Flash the release build"

# This is a special target that tells make to delete a file if an error occurs
# while the file is being generated.
.DELETE_ON_ERROR:
