## Secure bootloader Makefile and linker scripts

NOTE: The "--sd-req" option to give nrfutil when generating a package that includes a SoftDevice can be determined empirically by using the [sd_info_struct.py script](https://github.com/inductivekickback/nrf-toolchain/blob/master/utils/sd_info_struct.py) to read the SD_FWID:

```
python2 sd_info_struct.py ../../Nordic-Thingy52-FW/external/sdk/components/softdevice/s332/hex/ANT_s332_nrf52_2.0.1.hex

SoftDevice information structure for 'ANT_s332_nrf52_2.0.1.hex':
  SD_SIZE:    0x29000
  SD_FWID:    0x8e
  SD_ID:      332
  SD_VERSION: 2.0.1
```

NOTE: The debug version of the bootloader is larger and will therefore be placed at a lower flash address than the release version. This means that [UICR.BOOTLOADERADDR](http://infocenter.nordicsemi.com/index.jsp?topic=%2Fcom.nordic.infocenter.s140.sds%2Fdita%2Fsoftdevices%2Fs130%2Fmbr_bootloader%2Fmbr_sd_reset_behavior.html&resultof=%22%4d%42%52%22%20%22%6d%62%72%22%20%22%72%65%73%65%74%22%20) needs to be erased and rewritten when switching between the debug and release builds.

The easiest method for erasing the chip and UICR.BOOTLOADERADDR is via nrfjprog:
```
nrfjprog --recover
```

Then flash the SoftDevice (s132_nrf52_4.0.2_softdevice.hex):
```
make flash_sd
```

Next, flash the desired version of the bootloader:
```
make flash_debug
```
or
```
make flash_release
```

The LED on the Thingy:52 should now be pulsing green to signify that it is in bootloader mode. New firmware can be loaded OTA at this point.

The firmware can also be programmed to the device via the debug probe. The next steps assume that the application has been built and is named "ble_app_thingy_s132_pca20020.hex".

Generate a settings page:
```
nrfutil settings generate --application ble_app_thingy_s132_pca20020.hex --family NRF52 --application-version 1 --bootloader-version 1 --bl-settings-version 1 settings.hex
```

Program the application (from the pca20020_s132 project directory):
```
make flash_debug
```
or
```
make flash_release
```

Program the settings page:
```
nrfjprog --program settings.hex --sectorerase
```

Finaly, reset the board to run the application:
```
nrfjprog -r
```

The LED on the Thingy:52 should now be pulsing blue.
