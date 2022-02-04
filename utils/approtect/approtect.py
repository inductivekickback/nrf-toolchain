"""
Add a value to a hex file to configure APPROTECT on nRF52 devices.
"""
import sys
import argparse
import struct
import intelhex


APPROTECT_ADDR = 0x10001208
APPROTECT_ENABLE = 0xFFFFFF00
APPROTECT_DISABLE = 0xFFFFFF5A


def _add_and_parse_args():
    """Build the argparse object and parse the args."""
    parser = argparse.ArgumentParser(prog='approtect',
                                     description=('A command line utility for configuring ' +
                                                  'APPROTECT in nRF52 hex files.'),
                                     epilog=('WARNING: Only for use with nRF52805 revision 2 ' +
                                             '(build codes Bx0), nRF52810 revision 3 (build codes' +
                                             ' Ex0), nrf52811 revision 2 (build codes Bx0), ' +
                                             'nRF52820 revision 3 (build codes Dx0), nRF52833 ' +
                                             'revision 2 (build codes Bx0), nRF52832 revision 3 ' +
                                             '(build codes Gx0), and nRF52840 revision 3 ' +
                                             '(build codes Fx0).'))
    parser.add_argument("-i", "--infile", type=str, default=None, metavar="INPUT_HEX_FILE",
                        required=True, help="path to hex file that will be configured")
    parser.add_argument("-o", "--outfile", type=str, default=None, metavar="OUTPUT_HEX_FILE",
                        required=True, help="path where modified hex file will be saved")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-d", "--disable", action='store_true',
                       help="disable access port protection (keep device unlocked)")
    group.add_argument("-e", "--enable", action='store_true',
                       help="enable access port protection (lock device)")

    args = parser.parse_args()
    if not args.enable and not args.disable:
        parser.print_usage()
        print("error: one of --enable or --disable is required")
        sys.exit(-1)

    return args


def _find_existing_config(intel_hex_file):
    """Print a warning if the hex file already contains an APPROTECT config."""
    try:
        setting = intel_hex_file.gets(APPROTECT_ADDR, 4)
        setting = struct.unpack("<L", setting)[0]
        if setting == APPROTECT_ENABLE:
            print("warning: infile contained the ENABLE APPROTECT value to lock the device")
        elif setting == APPROTECT_DISABLE:
            print("warning: infile contained the DISABLE APPROTECT value to unlock the device")
        else:
            print("warning: infile contained an invalid APPROTECT value ({})".format(hex(setting)))
    except intelhex.NotEnoughDataError:
        pass


def _main():
    """Parses arguments for the CLI."""
    args = _add_and_parse_args()
    try:
        intel_hex_file = intelhex.IntelHex(args.infile)
        _find_existing_config(intel_hex_file)
        if args.enable:
            intel_hex_file.puts(APPROTECT_ADDR, struct.pack("<L", APPROTECT_ENABLE))
        else:
            intel_hex_file.puts(APPROTECT_ADDR, struct.pack("<L", APPROTECT_DISABLE))
        intel_hex_file.write_hex_file(args.outfile)
        sys.exit(0)
    except Exception as ex:
        print("error: " + str(ex))
        sys.exit(-1)


if __name__ == "__main__":
    _main()
