# nrf-toolchain
Makefiles (GNU Make) and other toolchain artifacts.

## For SDK 13 and 14.2:
NOTE: This version of the Makefile has been tested under Windows 10 using the standard command shell as well as Ubuntu using Bash. **If Cygwin is used on a Windows machine then ctrl-c will cause GDB to terminate instead of triggering a breakpoint trap.**
- Support for using [Monitor Mode Debugging](https://devzone.nordicsemi.com/blogs/1088/monitor-mode-debugging-with-j-link-and-gdbeclipse/) with J-Links was added.
  - Requires a J-Link PLUS, ULTRA+, or PRO when using Linux or OSX. Can be evaluated using a J-Link Lite on Windows by accepting a license pop-up. **The J-Link driver silently falls back to Halt mode on Linux/OSX when using a J-Link Lite (including the J-Link that is included on Nordic development kits).**
  - Requires copying three files from the 'Sample project' [here](https://www.segger.com/monitor-mode-debugging.html):
    - Create a new dir e.g. {SDK_ROOT}/external/jlink_monitor_mode_debug/gcc
    - Copy JLINK_MONITOR.c, JLINK_MONITOR.h, and JLINK_MONITOR_ISR_SES.s from the 'Sample project' to the new dir
    - Set JLINK_MON_DEBUG_DIR at the top of the Makefile to point to the new dir
  - Requires calling `NVIC_SetPriority(DebugMonitor_IRQn, 7UL);`early (e.g. at the top of main).
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
