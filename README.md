# nrf-toolchain
Makefiles and other toolchain artifacts.

## For SDK 11:
- The original "components/toolchain/gcc/Makefile.posix" needs to be replaced with mine to fix a delimiting problem

## For SDK 12:
- "components/toolchain/gcc/gcc_startup_nrf52.S" needs to be renamed to "components/toolchain/gcc/gcc_startup_nrf52.s"

- ### For SDK 12.2
  - The BSP files have been moved. So "/components/libraries/bsp" and "/components/boards" need to be added to INC_DIRS, "/components/boards/boards.c" needs to be added to SRC_FILES, and the paths for "bsp.c" and "bsp_btn_ble.c" need to be updated to "/components/libraries/bsp/".

## For SDK 13:
- "components/toolchain/gcc/gcc_startup_nrf52.S" needs to be renamed to "components/toolchain/gcc/gcc_startup_nrf52.s"
- An example Makefile for using Monitor Mode Debugging with J-Links was added.
  - Requires a J-Link PLUS, ULTRA+, or PRO when using Linux or OSX
  - Requires copying three files from the 'Sample project' [here](https://www.segger.com/monitor-mode-debugging.html):
    - Create a new dir at {SDK13_ROOT}/external/jlink_monitor_mode_debug/gcc
    - Copy JLINK_MONITOR.c, JLINK_MONITOR.h, and JLINK_MONITOR_ISR_SES.s to the new dir
  - 'make gdb' will compile without the Monitor Mode files and start GDB in halt mode
  - 'make MMD=1 gdb' will compile with the Monitor Mode files and start GDB in Monitor mode
