# Note: This works as of S132 v3.0.0 at least.

import sys
import os
from intelhex import IntelHex


def _read_u32(ih, addr):
    return ((_read_u16(ih, addr + 2) << 16) | _read_u16(ih, addr))


def _read_u16(ih, addr):
    return ((ih[addr + 1] << 8) | ih[addr])


def _read_sd_version(ih, addr):
    value = _read_u32(ih, addr)
    return ('%d.%d.%d' % ((value / 1000000), ((value % 1000000) / 1000), (value % 1000)))


# See nrf_sdm.h for more information.
SOFTDEVICE_INFO_STRUCT_ADDRESS = 0x3000

SD_MAGIC_NUMBER_VALUE = 0x51B1E5DB
SD_MAGIC_NUMBER_OFFSET = 0x04

# Each tuple is the description, offset, and length in bytes.
INFO_STRUCT_TUPLES = (('SD_SIZE',    0x08, lambda x, y: hex(_read_u32(x,y))),
                      ('SD_FWID',    0x0C, lambda x, y: hex(_read_u16(x,y))),
                      ('SD_ID',      0x10, lambda x, y: str(_read_u32(x,y))),
                      ('SD_VERSION', 0x14, _read_sd_version))


if ("__main__" == __name__):
    if (2 == len(sys.argv)):
        file_name = sys.argv[1]
    else:
        print "ERROR: Usage is 'python sd_info_struct.py <file_name>'."
        sys.exit(-1)

    ih = IntelHex()
    try:
        if (file_name.lower().endswith('.hex')):
            ih.loadhex(file_name)
        else:
            ih.loadbin(file_name)
    except:
        print "ERROR: Could not open the data file."
        sys.exit(-1)

    magic_number = _read_u32(ih, (SOFTDEVICE_INFO_STRUCT_ADDRESS + SD_MAGIC_NUMBER_OFFSET))
    if (SD_MAGIC_NUMBER_VALUE != magic_number):
        print "ERROR: SD magic number not found."
        sys.exit(-1)

    print "\nSoftDevice information structure for '%s':" % os.path.basename(file_name)
    for t in INFO_STRUCT_TUPLES:
        print '  {0:<12}{1}'.format(t[0] + ':', t[2](ih, (SOFTDEVICE_INFO_STRUCT_ADDRESS + t[1])))

    sys.exit(0)
