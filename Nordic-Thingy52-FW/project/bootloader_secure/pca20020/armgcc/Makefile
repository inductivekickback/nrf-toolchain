# The PROJECT_NAME can be changed arbitrarily (it does not depend on anything).
PROJECT_NAME := secure_dfu_thingy_s332_pca20020

DBG_BUILD_DIR := ./_debug
REL_BUILD_DIR := ./_release
DEPS_DIR := ./_deps

SDK_ROOT := ../../../..
PROJ_DIR := ../..
COMPONENTS_DIR := $(SDK_ROOT)/external/sdk/components
SOURCE_DIR := $(SDK_ROOT)/source
LIBS_DIR := $(SDK_ROOT)/libs
EXTERNAL_DIR := $(SDK_ROOT)/external
INCLUDE_DIR := $(SDK_ROOT)/include

# JLINK_MON_DEBUG_DIR should point to the directory that contains the files
# in JLINK_MON_DEBUG_FILES plus JLINK_MONITOR.h. If Monitor Mode Debugging is
# not required then leave JLINK_MON_DEBUG_DIR empty.
JLINK_MON_DEBUG_DIR := 

# If the JLINK_MON_DEBUG_DIR is empty then make sure it is evaluated correctly.
JLINK_MON_DEBUG_DIR := $(strip $(JLINK_MON_DEBUG_DIR))

# These are the required files as of version 6.12a of the J-Link driver.
JLINK_MON_DEBUG_FILES := JLINK_MONITOR.c JLINK_MONITOR_ISR_SES.s

# The offset of the application needs to be specified so the J-Link knows
# the location of the DebugMon_Handler.
JLINK_MON_DEBUG_APP_FLASH_LOCATION := 0x6f000

# Init commands will be written to a file and then specified when starting GDB
# instead of relying on .gdbinit (to avoid having to enable .gbdinit files).
GDB_CMD_PATH := $(DBG_BUILD_DIR)/gdb.txt

SD_HEX_PATH := $(COMPONENTS_DIR)/softdevice/s332/hex/ANT_s332_nrf52_2.0.1.hex

# Include the correct template Makefile depending on platform.
TEMPLATE_PATH = $(COMPONENTS_DIR)/toolchain/gcc
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
	-DNRF52 \
	-DSWI_DISABLE0 \
	-DS332 \
	-DSOFTDEVICE_PRESENT \
	-DBLE_STACK_SUPPORT_REQD \
	-DANT_STACK_SUPPORT_REQD \
	-DNRF_LOG_USES_RTT=1 \
	-DSVC_INTERFACE_CALL_AS_NORMAL_FUNCTION \
	-DBOARD_PCA20020 \
	-DCONFIG_GPIO_AS_PINRESET

CFLAGS += \
	-DNRF52832 \
	-DNRF_SD_BLE_API_VERSION=3 \
	-D__HEAP_SIZE \
	-DBLE_DFU_APP_SUPPORT \
	-DNRF_DFU_SETTINGS_VERSION=1 \
	-mcpu=cortex-m4 \
	-mthumb \
	-Wall \
	-mfloat-abi=hard \
	-mfpu=fpv4-sp-d16 \
	-ffunction-sections \
	-fdata-sections \
	-fno-strict-aliasing \
	-fno-builtin \
	-mabi=aapcs \
	--short-enums \
	--std=gnu99 \
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
	-mcpu=cortex-m4 \
	-mfloat-abi=hard \
	-mfpu=fpv4-sp-d16 \
	-Wl,--gc-sections \
	--specs=nano.specs

# Add standard libraries at the very end of the linker input, after all objects
# that may need symbols provided by these libraries.
LIB_FILES += \
	$(EXTERNAL_DIR)/sdk/external/micro-ecc/nrf52_armgcc/armgcc/micro_ecc_lib_nrf52.a \
	-lc \
	-lnosys \
	-lm

SRC_FILES += \
	$(COMPONENTS_DIR)/libraries/util/app_error_weak.c \
	$(COMPONENTS_DIR)/libraries/fifo/app_fifo.c \
	$(COMPONENTS_DIR)/libraries/scheduler/app_scheduler.c \
	$(COMPONENTS_DIR)/libraries/timer/app_timer.c \
	$(COMPONENTS_DIR)/libraries/timer/app_timer_appsh.c \
	$(COMPONENTS_DIR)/libraries/util/app_util_platform.c \
	$(COMPONENTS_DIR)/libraries/crc32/crc32.c \
	$(COMPONENTS_DIR)/libraries/ecc/ecc.c \
	$(COMPONENTS_DIR)/libraries/fstorage/fstorage.c \
	$(COMPONENTS_DIR)/libraries/hci/hci_mem_pool.c \
	$(COMPONENTS_DIR)/libraries/util/nrf_assert.c \
	$(COMPONENTS_DIR)/libraries/crypto/nrf_crypto.c \
	$(COMPONENTS_DIR)/libraries/sha256/sha256.c \
	$(COMPONENTS_DIR)/drivers_nrf/common/nrf_drv_common.c \
	$(COMPONENTS_DIR)/drivers_nrf/rng/nrf_drv_rng.c \
	$(COMPONENTS_DIR)/drivers_nrf/hal/nrf_nvmc.c \
	$(COMPONENTS_DIR)/libraries/bootloader/ble_dfu/nrf_ble_dfu.c \
	$(PROJ_DIR)/dfu-cc.pb.c \
	$(PROJ_DIR)/keys/public_key.c \
	$(PROJ_DIR)/dfu_req_handling.c \
	$(PROJ_DIR)/main.c \
	$(COMPONENTS_DIR)/ble/common/ble_advdata.c \
	$(COMPONENTS_DIR)/ble/common/ble_conn_params.c \
	$(COMPONENTS_DIR)/ble/common/ble_srv_common.c \
	$(EXTERNAL_DIR)/nano-pb/pb_common.c \
	$(EXTERNAL_DIR)/nano-pb/pb_decode.c \
	$(COMPONENTS_DIR)/toolchain/system_nrf52.c \
	$(COMPONENTS_DIR)/softdevice/common/softdevice_handler/softdevice_handler.c \
	$(COMPONENTS_DIR)/softdevice/common/softdevice_handler/softdevice_handler_appsh.c \
	$(COMPONENTS_DIR)/libraries/bootloader/nrf_bootloader.c \
	$(COMPONENTS_DIR)/libraries/bootloader/nrf_bootloader_app_start.c \
	$(COMPONENTS_DIR)/libraries/bootloader/nrf_bootloader_info.c \
	$(COMPONENTS_DIR)/libraries/bootloader/dfu/nrf_dfu.c \
	$(COMPONENTS_DIR)/libraries/bootloader/dfu/nrf_dfu_flash.c \
	$(COMPONENTS_DIR)/libraries/bootloader/dfu/nrf_dfu_mbr.c \
	$(COMPONENTS_DIR)/libraries/bootloader/dfu/nrf_dfu_settings.c \
	$(COMPONENTS_DIR)/libraries/bootloader/dfu/nrf_dfu_transport.c \
	$(COMPONENTS_DIR)/libraries/bootloader/dfu/nrf_dfu_utils.c \
	$(COMPONENTS_DIR)/drivers_nrf/twi_master/nrf_drv_twi.c \
	$(SOURCE_DIR)/drivers/drv_ext_light.c \
	$(SOURCE_DIR)/drivers/drv_sx1509.c \
	$(SOURCE_DIR)/util/sx150x_led_drv_calc.c \
	$(SOURCE_DIR)/util/twi_manager.c \
	$(EXTERNAL_DIR)/segger_rtt/RTT_Syscalls_GCC.c \
	$(EXTERNAL_DIR)/segger_rtt/SEGGER_RTT.c \
	$(EXTERNAL_DIR)/segger_rtt/SEGGER_RTT_printf.c \
	$(COMPONENTS_DIR)/toolchain/gcc/gcc_startup_nrf52.S

INC_DIRS += \
	$(COMPONENTS_DIR)/toolchain/cmsis/include \
	$(COMPONENTS_DIR)/drivers_nrf/rng \
	$(COMPONENTS_DIR)/toolchain \
	$(COMPONENTS_DIR)/device \
	$(COMPONENTS_DIR)/drivers_nrf/hal \
	$(COMPONENTS_DIR)/libraries/sha256 \
	$(COMPONENTS_DIR)/libraries/crc32 \
	$(COMPONENTS_DIR)/libraries/experimental_section_vars \
	$(PROJ_DIR) \
	$(COMPONENTS_DIR)/libraries/fstorage \
	$(COMPONENTS_DIR)/libraries/util \
	$(COMPONENTS_DIR) \
	$(COMPONENTS_DIR)/softdevice/common/softdevice_handler \
	$(COMPONENTS_DIR)/libraries/timer \
	$(COMPONENTS_DIR)/drivers_nrf/clock \
	../config \
	$(COMPONENTS_DIR)/softdevice/s332/headers/nrf52 \
	$(COMPONENTS_DIR)/libraries/log/src \
	$(COMPONENTS_DIR)/libraries/bootloader/dfu \
	$(COMPONENTS_DIR)/drivers_nrf/delay \
	$(COMPONENTS_DIR)/ble/common \
	$(COMPONENTS_DIR)/libraries/fifo \
	$(COMPONENTS_DIR)/libraries/bootloader/ble_dfu \
	$(COMPONENTS_DIR)/libraries/svc \
	$(COMPONENTS_DIR)/libraries/log \
	$(COMPONENTS_DIR)/libraries/hci \
	$(COMPONENTS_DIR)/libraries/scheduler \
	$(COMPONENTS_DIR)/libraries/bootloader \
	$(COMPONENTS_DIR)/libraries/crypto \
	$(COMPONENTS_DIR)/softdevice/s332/headers \
	$(COMPONENTS_DIR)/drivers_nrf/common \
	$(EXTERNAL_DIR)/sdk/external/micro-ecc/micro-ecc \
	$(COMPONENTS_DIR)/libraries/bootloader/ble_dfu \
	$(EXTERNAL_DIR)/nano-pb \
	$(COMPONENTS_DIR)/libraries/ecc \
	$(COMPONENTS_DIR)/toolchain/gcc \
	$(SDK_ROOT)/include/board \
	$(SDK_ROOT)/include/drivers \
	$(SDK_ROOT)/include/util \
	$(SDK_ROOT)/include/macros \
	$(SDK_ROOT)/include/modules \
	$(SDK_ROOT)/include/ble_services \
	$(EXTERNAL_DIR)/sdk/components/drivers_nrf/twi_master \
	$(EXTERNAL_DIR)/segger_rtt

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
default: CFLAGS += -O0 -ggdb -fomit-frame-pointer
default: OBJ_DIR := $(DBG_BUILD_DIR)
default: LINKER_SCRIPT := $(PROJ_DIR)/secure_dfu_gcc_nrf52_debug.ld
default: $(DBG_BUILD_DIR)/$(PROJECT_NAME).hex
	$(call echosize,$(DBG_BUILD_DIR)/$(PROJECT_NAME).out)

.PHONY: release
release: CFLAGS += -Os -g3 -flto
release: OBJ_DIR := $(REL_BUILD_DIR)
release: LINKER_SCRIPT := $(PROJ_DIR)/secure_dfu_gcc_nrf52.ld
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
