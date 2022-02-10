This is a simple command line tool that strips the MBR from SoftDevice hex files.

### Requirements
The intelhex module does all of the heavy lifting.
```
$ pip3 install --user intelhex
```

### Usage
The tool expects the path to a SoftDevice hex file as an input and a path for the hex file to use as the output. A third path can be specified if the MBR needs to be saved to its own hex file. **The input hex file is not modifed.**
```
$ python3 mbr_strip.py --help
usage: mbr_strip [-h] -i INPUT_HEX_FILE -o OUTPUT_HEX_FILE [-m MBR_HEX_FILE]

A command line utility for stripping the MBR out of a SoftDevice hex file.

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_HEX_FILE, --infile INPUT_HEX_FILE
                        path to hex file that contains an MBR
  -o OUTPUT_HEX_FILE, --outfile OUTPUT_HEX_FILE
                        path where modified hex file will be saved
  -m MBR_HEX_FILE, --mbr MBR_HEX_FILE
                        path where MBR hex file will be saved
```
The tool is silent:
```
$ python3 mbr_strip.py -i s113_nrf52_7.2.0_softdevice.hex -o s113_7.2.0_stripped.hex -m stripped_mbr_2.4.1.hex
```

### Testing
nrfjprog can be used to verify the integrity of the new hex files. First plug in an nRF52 DK and then:
```
$ python3 mbr_strip.py -i s113_nrf52_7.2.0_softdevice.hex -o s113_7.2.0_stripped.hex -m stripped_mbr_2.4.1.hex
$ nrfjprog --recover
Recovering device. This operation might take 30s.
Erasing user code and UICR flash areas.
$ nrfjprog --program stripped_mbr_2.4.1.hex --verify
Parsing image file.
Verifying programming.
Verified OK.
$ nrfjprog --program s113_7.2.0_stripped.hex --verify
Parsing image file.
Verifying programming.
Verified OK.
$ nrfjprog --readcode test.hex
Storing data in 'test.hex'.
$ nrfjprog --recover
Recovering device. This operation might take 30s.
Erasing user code and UICR flash areas.
$ nrfjprog --program s113_nrf52_7.2.0_softdevice.hex --verify
Parsing image file.
Verifying programming.
Verified OK.
$ nrfjprog --readcode control.hex
Storing data in 'control.hex'.
$ diff test.hex control.hex
```
