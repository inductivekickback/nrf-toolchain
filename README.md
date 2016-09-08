# nrf-toolchain
Makefiles and other toolchain artifacts.

## For SDK 11:
- The original "components/toolchain/gcc/Makefile.posix" needs to be replaced with mine to fix a delimiting problem

## For SDK 12:
- "components/toolchain/gcc/gcc_startup_nrf52.S" needs to be renamed to "components/toolchain/gcc/gcc_startup_nrf52.s"
