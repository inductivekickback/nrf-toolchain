# The PROJECT_NAME can be changed arbitrarily (it does not depend on anything).
PROJECT_NAME := ble_app_thingy_s132_pca20020

# The LINKER_SCRIPT is usually in the same directory as the Makefile.
LINKER_SCRIPT := ble_app_thingy_gcc_nrf52.ld

DBG_BUILD_DIR := ./_debug
REL_BUILD_DIR := ./_release
DEPS_DIR := ./_deps

SDK_ROOT := ../../..
PROJ_DIR := ..
COMPONENTS_DIR := $(SDK_ROOT)/sdk_components
SOURCE_DIR := $(SDK_ROOT)/source
LIBS_DIR := $(SDK_ROOT)/libs
EXTERNAL_DIR := $(SDK_ROOT)/external
INCLUDE_DIR := $(SDK_ROOT)/include

# JLINK_MON_DEBUG_DIR should point to the directory that contains the files
# in JLINK_MON_DEBUG_FILES plus JLINK_MONITOR.h. If Monitor Mode Debugging is
# not required then leave JLINK_MON_DEBUG_DIR empty.
JLINK_MON_DEBUG_DIR := 

# The offset of the application needs to be specified so the J-Link knows
# the location of the DebugMon_Handler. For the S132 v4 this is 0x1F000.
JLINK_MON_DEBUG_APP_FLASH_LOCATION := 0x1F000

# If the JLINK_MON_DEBUG_DIR is empty then make sure it is evaluated correctly.
JLINK_MON_DEBUG_DIR := $(strip $(JLINK_MON_DEBUG_DIR))

# These are the required files as of version 6.12a of the J-Link driver.
JLINK_MON_DEBUG_FILES := JLINK_MONITOR.c JLINK_MONITOR_ISR_SES.s

# Init commands will be written to a file and then specified when starting GDB
# instead of relying on .gdbinit (to avoid having to enable .gbdinit files).
GDB_CMD_PATH := $(DBG_BUILD_DIR)/gdb.txt

SD_HEX_PATH := $(COMPONENTS_DIR)/softdevice/s132/hex/s132_nrf52_4.0.2_softdevice.hex

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
	-DNRF52832_XXAA \
	-DSWI_DISABLE0 \
	-DS132 \
	-DSOFTDEVICE_PRESENT \
	-DBLE_STACK_SUPPORT_REQD \
	-DNRF_LOG_USES_RTT=1 \
	-DBSP_DEFINES_ONLY \
	-DARM_MATH_CM4 \
	-DMPU9250 \
	-DEMPL \
	-DUSE_DMP \
	-DEMPL_TARGET_NRF52

CFLAGS += \
	-DNRF52832 \
	-DNRF_SD_BLE_API_VERSION=4 \
	-D__HEAP_SIZE \
	-DBLE_DFU_APP_SUPPORT \
	-DNRF_DFU_SETTINGS_VERSION=1 \
	-DCONFIG_NFCT_PINS_AS_GPIOS \
	-DAUDIO_EQ_DEF=3 \
	-mcpu=cortex-m4 \
	-mthumb \
	--std=gnu99 \
	-Wall \
	-mfloat-abi=hard \
	-mfpu=fpv4-sp-d16 \
	-ffunction-sections \
	-fdata-sections \
	-fno-strict-aliasing \
	-fno-builtin \
	-fshort-enums \
	-mabi=aapcs \
	-DHAL_NFC_ENGINEERING_BC_FTPAN_WORKAROUND \
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
	$(LIBS_DIR)/liblibmplmpu_m4_hardfp/liblibmplmpu.a \
	$(COMPONENTS_DIR)/toolchain/cmsis/dsp/GCC/libarm_cortexM4lf_math.a \
	$(COMPONENTS_DIR)/nfc/t2t_lib/nfc_t2t_lib_gcc.a \
	-lc \
	-lnosys \
	-lm

SRC_FILES += \
	$(PROJ_DIR)/main.c \
	$(SOURCE_DIR)/modules/m_ble.c \
	$(SOURCE_DIR)/modules/m_ble_flash.c \
	$(SOURCE_DIR)/util/advertiser_beacon_timeslot.c \
	$(SOURCE_DIR)/util/twi_manager.c \
	$(SOURCE_DIR)/util/support_func.c \
	$(SOURCE_DIR)/modules/m_environment.c \
	$(SOURCE_DIR)/modules/m_environment_flash.c \
	$(SOURCE_DIR)/modules/m_sound.c \
	$(SOURCE_DIR)/modules/m_motion.c \
	$(SOURCE_DIR)/modules/m_motion_flash.c \
	$(SOURCE_DIR)/modules/m_ui.c \
	$(SOURCE_DIR)/modules/m_ui_flash.c \
	$(SOURCE_DIR)/modules/m_batt_meas.c \
	$(SOURCE_DIR)/drivers/drv_nfc.c \
	$(SOURCE_DIR)/drivers/drv_gas_sensor.c \
	$(SOURCE_DIR)/drivers/drv_ccs811.c \
	$(SOURCE_DIR)/drivers/drv_pressure.c \
	$(SOURCE_DIR)/drivers/drv_lps22hb.c \
	$(SOURCE_DIR)/drivers/drv_humidity.c \
	$(SOURCE_DIR)/drivers/drv_hts221.c \
	$(SOURCE_DIR)/drivers/drv_ext_light.c \
	$(SOURCE_DIR)/drivers/drv_ext_gpio.c \
	$(SOURCE_DIR)/util/sx150x_led_drv_calc.c \
	$(SOURCE_DIR)/drivers/drv_sx1509.c \
	$(SOURCE_DIR)/drivers/drv_bh1745.c \
	$(SOURCE_DIR)/drivers/drv_color.c \
	$(SOURCE_DIR)/drivers/drv_speaker.c \
	$(SOURCE_DIR)/drivers/drv_mpu9250.c \
	$(SOURCE_DIR)/drivers/drv_motion.c \
	$(SOURCE_DIR)/drivers/drv_acc_lis3dh.c \
	$(SOURCE_DIR)/drivers/drv_mic.c \
	$(LIBS_DIR)/eMD6/core/driver/eMPL/inv_mpu.c \
	$(LIBS_DIR)/eMD6/core/driver/eMPL/inv_mpu_dmp_motion_driver.c \
	$(LIBS_DIR)/eMD6/core/mllite/data_builder.c \
	$(LIBS_DIR)/eMD6/core/mllite/hal_outputs.c \
	$(LIBS_DIR)/eMD6/core/mllite/message_layer.c \
	$(LIBS_DIR)/eMD6/core/mllite/ml_math_func.c \
	$(LIBS_DIR)/eMD6/core/mllite/mlmath.c \
	$(LIBS_DIR)/eMD6/core/mllite/mpl.c \
	$(LIBS_DIR)/eMD6/core/mllite/results_holder.c \
	$(LIBS_DIR)/eMD6/core/mllite/start_manager.c \
	$(LIBS_DIR)/eMD6/core/mllite/storage_manager.c \
	$(LIBS_DIR)/eMD6/core/eMPL-hal/eMPL_outputs.c \
	$(LIBS_DIR)/eMD6/core/driver/nRF52/log_nrf52.c \
	$(LIBS_DIR)/dvi_adpcm/dvi_adpcm.c \
	$(LIBS_DIR)/sr3_audio/drv_audio_coder_adpcm.c \
	$(LIBS_DIR)/sr3_audio/drv_audio_coder_bv32fp.c \
	$(LIBS_DIR)/sr3_audio/drv_audio_dsp.c \
	$(LIBS_DIR)/sr3_audio/drv_audio_pdm.c \
	$(COMPONENTS_DIR)/ble/common/ble_advdata.c \
	$(COMPONENTS_DIR)/ble/ble_advertising/ble_advertising.c \
	$(COMPONENTS_DIR)/ble/common/ble_conn_params.c \
	$(COMPONENTS_DIR)/ble/common/ble_srv_common.c \
	$(COMPONENTS_DIR)/ble/common/ble_conn_state.c \
	$(SOURCE_DIR)/ble_services/ble_tes.c \
	$(SOURCE_DIR)/ble_services/ble_tcs.c \
	$(SOURCE_DIR)/ble_services/ble_uis.c \
	$(SOURCE_DIR)/ble_services/ble_tms.c \
	$(SOURCE_DIR)/ble_services/ble_tss.c \
	$(COMPONENTS_DIR)/drivers_nrf/common/nrf_drv_common.c \
	$(COMPONENTS_DIR)/drivers_nrf/gpiote/nrf_drv_gpiote.c \
	$(COMPONENTS_DIR)/drivers_nrf/twi_master/nrf_drv_twi.c \
	$(COMPONENTS_DIR)/drivers_nrf/pwm/nrf_drv_pwm.c \
	$(COMPONENTS_DIR)/drivers_nrf/pdm/nrf_drv_pdm.c \
	$(COMPONENTS_DIR)/drivers_nrf/clock/nrf_drv_clock.c \
	$(COMPONENTS_DIR)/drivers_nrf/saadc/nrf_drv_saadc.c \
	$(COMPONENTS_DIR)/drivers_nrf/hal/nrf_saadc.c \
	$(COMPONENTS_DIR)/drivers_nrf/rng/nrf_drv_rng.c \
	$(COMPONENTS_DIR)/nfc/ndef/launchapp/nfc_launchapp_msg.c) \
	$(COMPONENTS_DIR)/nfc/ndef/launchapp/nfc_launchapp_rec.c) \
	$(COMPONENTS_DIR)/nfc/ndef/uri/nfc_uri_msg.c) \
	$(COMPONENTS_DIR)/nfc/ndef/uri/nfc_uri_rec.c) \
	$(COMPONENTS_DIR)/nfc/ndef/generic/message/nfc_ndef_msg.c) \
	$(COMPONENTS_DIR)/nfc/ndef/generic/record/nfc_ndef_record.c) \
	$(COMPONENTS_DIR)/nfc/ndef/text/nfc_text_rec.c) \
	$(COMPONENTS_DIR)/nfc/t2t_lib/hal_t2t/hal_nfc_t2t.c) \
	$(COMPONENTS_DIR)/libraries/button/app_button.c \
	$(COMPONENTS_DIR)/libraries/util/app_error.c \
	$(COMPONENTS_DIR)/libraries/scheduler/app_scheduler.c \
	$(COMPONENTS_DIR)/libraries/timer/app_timer.c \
	$(COMPONENTS_DIR)/libraries/util/nrf_assert.c \
	$(COMPONENTS_DIR)/libraries/uart/retarget.c \
	$(COMPONENTS_DIR)/libraries/led_softblink/led_softblink.c \
	$(COMPONENTS_DIR)/libraries/low_power_pwm/low_power_pwm.c \
	$(COMPONENTS_DIR)/libraries/fstorage/fstorage.c \
	$(COMPONENTS_DIR)/libraries/fds/fds.c \
	$(COMPONENTS_DIR)/libraries/util/app_util_platform.c \
	$(COMPONENTS_DIR)/libraries/util/sdk_mapped_flags.c \
	$(COMPONENTS_DIR)/libraries/queue/nrf_queue.c \
	$(EXTERNAL_DIR)/segger_rtt/RTT_Syscalls_GCC.c \
	$(EXTERNAL_DIR)/segger_rtt/SEGGER_RTT.c \
	$(EXTERNAL_DIR)/segger_rtt/SEGGER_RTT_printf.c \
	$(COMPONENTS_DIR)/softdevice/common/softdevice_handler/softdevice_handler.c \
	$(COMPONENTS_DIR)/toolchain/system_nrf52.c \
	$(COMPONENTS_DIR)/libraries/log/src/nrf_log_frontend.c \
	$(COMPONENTS_DIR)/libraries/log/src/nrf_log_backend_serial.c \
	$(SOURCE_DIR)/util/nrf_dfu_flash_buttonless.c \
	$(COMPONENTS_DIR)/ble/ble_services/ble_dfu/ble_dfu.c \
	$(COMPONENTS_DIR)/ble/ble_services/ble_bas/ble_bas.c \
	$(COMPONENTS_DIR)/libraries/bootloader/dfu/nrf_dfu_settings.c \
	$(COMPONENTS_DIR)/libraries/crc32/crc32.c \
	$(COMPONENTS_DIR)/libraries/strerror/nrf_strerror.c) \
	$(EXTERNAL_DIR)/sdk13_override/softdevice_handler_appsh.c \
	$(COMPONENTS_DIR)/toolchain/gcc/gcc_startup_nrf52.S

INC_DIRS += \
	$(COMPONENTS_DIR)/device \
	$(COMPONENTS_DIR)/toolchain/cmsis/include \
	$(COMPONENTS_DIR)/toolchain/gcc \
	$(COMPONENTS_DIR)/toolchain \
	$(PROJ_DIR)/config \
	$(COMPONENTS_DIR)/ble/ble_advertising \
	$(COMPONENTS_DIR)/ble/common \
	$(EXTERNAL_DIR)/segger_rtt \
	$(COMPONENTS_DIR)/drivers_nrf/common \
	$(COMPONENTS_DIR)/drivers_nrf/clock \
	$(COMPONENTS_DIR)/drivers_nrf/saadc \
	$(COMPONENTS_DIR)/drivers_nrf/config \
	$(COMPONENTS_DIR)/drivers_nrf/delay \
	$(COMPONENTS_DIR)/drivers_nrf/gpiote \
	$(COMPONENTS_DIR)/drivers_nrf/hal \
	$(COMPONENTS_DIR)/drivers_nrf/pstorage \
	$(COMPONENTS_DIR)/drivers_nrf/uart \
	$(COMPONENTS_DIR)/drivers_nrf/pdm \
	$(COMPONENTS_DIR)/drivers_nrf/twi_master \
	$(COMPONENTS_DIR)/libraries/button \
	$(COMPONENTS_DIR)/libraries/fifo \
	$(COMPONENTS_DIR)/libraries/timer \
	$(COMPONENTS_DIR)/libraries/uart \
	$(COMPONENTS_DIR)/libraries/util \
	$(COMPONENTS_DIR)/libraries/log/src \
	$(COMPONENTS_DIR)/libraries/log \
	$(COMPONENTS_DIR)/libraries/fstorage \
	$(COMPONENTS_DIR)/libraries/fds \
	$(COMPONENTS_DIR)/libraries/bootloader/dfu \
	$(COMPONENTS_DIR)/libraries/experimental_section_vars \
	$(COMPONENTS_DIR)/libraries/crc32 \
	$(COMPONENTS_DIR)/libraries/led_softblink \
	$(COMPONENTS_DIR)/libraries/low_power_pwm \
	$(COMPONENTS_DIR)/nfc/ndef/generic/record \
	$(COMPONENTS_DIR)/nfc/ndef/generic/message \
	$(COMPONENTS_DIR)/nfc/ndef/launchapp \
	$(COMPONENTS_DIR)/nfc/ndef/uri \
	$(COMPONENTS_DIR)/nfc/ndef/text \
	$(COMPONENTS_DIR)/nfc/t2t_lib \
	$(COMPONENTS_DIR)/nfc/ndef/text \
	$(COMPONENTS_DIR)/softdevice/common/softdevice_handler \
	$(COMPONENTS_DIR)/softdevice/s132/headers \
	$(COMPONENTS_DIR)/softdevice/s132/headers/nrf52 \
	$(COMPONENTS_DIR)/ble/ble_services/ble_dfu \
	$(COMPONENTS_DIR)/ble/ble_services/ble_bas \
	$(INCLUDE_DIR)/ble_services \
	$(INCLUDE_DIR)/drivers \
	$(INCLUDE_DIR)/board \
	$(INCLUDE_DIR)/modules \
	$(INCLUDE_DIR)/macros \
	$(INCLUDE_DIR)/util \
	$(COMPONENTS_DIR)/libraries/scheduler \
	$(COMPONENTS_DIR)/libraries/fstorage \
	$(COMPONENTS_DIR)/libraries/experimental_section_vars \
	$(COMPONENTS_DIR)/drivers_nrf/pwm \
	$(SDK_ROOT)/tools/sound \
	$(LIBS_DIR)/eMD6/core/driver/include \
	$(LIBS_DIR)/eMD6/core/driver/eMPL \
	$(LIBS_DIR)/eMD6/core/mpl \
	$(LIBS_DIR)/eMD6/core/mllite \
	$(LIBS_DIR)/eMD6/core/eMPL-hal \
	$(LIBS_DIR)/eMD6/core/driver/nRF52 \
	$(LIBS_DIR)/sr3_audio \
	$(LIBS_DIR)/dvi_adpcm \
	$(LIBS_DIR)/bv32fp-1.2 \
	$(COMPONENTS_DIR)/drivers_nrf/rng \
	$(COMPONENTS_DIR)/libraries/queue

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
default: CFLAGS += -O0 -ggdb -DDEBUG
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
