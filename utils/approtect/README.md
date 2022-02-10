This is a simple command line tool that adds an NRF_UICR->APPROTECT value to nRF52-series hex files.

### Requirements
The intelhex module does all of the heavy lifting.
```
$ pip3 install --user intelhex
```

### Usage
The tool expects the path to a hex file as an input, a path to use for the output hex file, and whether the access port protection should be enabled or disabled.
```
$ python3 approtect.py --help
usage: approtect [-h] -i INPUT_HEX_FILE -o OUTPUT_HEX_FILE [-d | -e]

A command line utility for configuring APPROTECT in nRF52 hex files.

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_HEX_FILE, --infile INPUT_HEX_FILE
                        path to hex file that will be configured
  -o OUTPUT_HEX_FILE, --outfile OUTPUT_HEX_FILE
                        path where modified hex file will be saved
  -d, --disable         disable access port protection (keep device unlocked)
  -e, --enable          enable access port protection (lock device)

WARNING: Only for use with nRF52805 revision 2 (build codes Bx0), nRF52810 revision 3 (build codes Ex0), nrf52811 revision 2 (build codes Bx0),
nRF52820 revision 3 (build codes Dx0), nRF52833 revision 2 (build codes Bx0), nRF52832 revision 3 (build codes Gx0), and nRF52840 revision 3
(build codes Fx0).

```
The tool is usually silent:
```
$ python3 approtect.py -i ./zephyr.hex -o app_w_uicr.hex --disable
```
However, if the input hex file already contains an APPROTECT setting then a warning will be printed.
```
$ python3 approtect.py -i app_w_uicr.hex -o app_w_uicr.hex -d
warning: infile contained the DISABLE APPROTECT value to unlock the device
```

### Testing
Functionality can be verified directly:
```
$ python3 approtect.py -i zephyr.hex -o app_w_uicr.hex --enable
$ nrfjprog --recover
Recovering device. This operation might take 30s.
Writing image to disable ap protect.
Erasing user code and UICR flash areas.
$ nrfjprog --memrd 0x10001208
0x10001208: 0000005A                              |Z...|
$ nrfjprog --program app_w_uicr.hex 
Parsing image file.
Applying system reset.
Verified OK.
$ nrfjprog --memrd 0x10001208
0x10001208: 00000000                              |....|
```
