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
