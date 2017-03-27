# nrf-toolchain
Makefiles (GNU Make) and other toolchain artifacts.

## For SDK 13:
- Support for using [Monitor Mode Debugging](https://devzone.nordicsemi.com/blogs/877/monitor-mode-debugging-revolutionize-the-way-you-d/) with J-Links was added.
  - Requires a J-Link PLUS, ULTRA+, or PRO when using Linux or OSX. Can be evaluated using a J-Link Lite on Windows by accepting a license pop-up. **The J-Link driver silently falls back to Halt mode on Linux/OSX when using a J-Link Lite.**
  - Requires copying three files from the 'Sample project' [here](https://www.segger.com/monitor-mode-debugging.html):
    - Create a new dir e.g. {SDK13_ROOT}/external/jlink_monitor_mode_debug/gcc
    - Copy JLINK_MONITOR.c, JLINK_MONITOR.h, and JLINK_MONITOR_ISR_SES.s from the 'Sample project' to the new dir
    - Set JLINK_MON_DEBUG_DIR at the top of the Makefile to point to the new dir
  - Requires adding `NVIC_SetPriority(DebugMonitor_IRQn, 7UL);`to the top of main.c.
    - The priority needs to be set one level higher than the priority of the code to be debugged (e.g. priority 7 for debugging Thread level, priority 6 for debugging APP_LOW, etc).
  - Debug builds will compile with the Monitor Mode files and 'make release' will exclude them.

Update the debug build and launch GDB in Halt mode:
```
make gdb
```

Update the debug build and launch GDB in Monitor mode:
```
make gdb_mon
```

Segger's RTT Client can be launched by appending '_rtt' to the target:
```
make gdb_rtt
```
```
make gdb_mon_rtt
```

## For SDK 12:
- "components/toolchain/gcc/gcc_startup_nrf52.S" needs to be renamed to "components/toolchain/gcc/gcc_startup_nrf52.s"

- ### For SDK 12.2
  - The BSP files have been moved. So "/components/libraries/bsp" and "/components/boards" need to be added to INC_DIRS, "/components/boards/boards.c" needs to be added to SRC_FILES, and the paths for "bsp.c" and "bsp_btn_ble.c" need to be updated to "/components/libraries/bsp/".

## For SDK 11:
- The original "components/toolchain/gcc/Makefile.posix" needs to be replaced with mine to fix a delimiting problem
