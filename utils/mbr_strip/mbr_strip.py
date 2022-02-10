"""
Removes the MBR from a SoftDevice hex file
"""
import sys
import argparse
import intelhex


MBR_SIZE_BYTES = 4096


def _add_and_parse_args():
    """Build the argparse object and parse the args."""
    parser = argparse.ArgumentParser(prog='mbr_strip',
                                     description=('A command line utility for stripping the MBR ' +
                                                  'out of a SoftDevice hex file.'))
    parser.add_argument("-i", "--infile", type=str, default=None, metavar="INPUT_HEX_FILE",
                        required=True, help="path to hex file that contains an MBR")
    parser.add_argument("-o", "--outfile", type=str, default=None, metavar="OUTPUT_HEX_FILE",
                        required=True, help="path where modified hex file will be saved")
    parser.add_argument("-m", "--mbr", type=str, default=None, metavar="MBR_HEX_FILE",
                        required=False, help="path where MBR hex file will be saved")
    return parser.parse_args()


def _main():
    """Parses arguments for the CLI."""
    args = _add_and_parse_args()
    try:
        intel_hex_file = intelhex.IntelHex(args.infile)

        out = intel_hex_file[MBR_SIZE_BYTES:]
        out.write_hex_file(args.outfile)

        if args.mbr:
            mbr = intel_hex_file[:MBR_SIZE_BYTES]
            mbr.write_hex_file(args.mbr)

        sys.exit(0)
    except Exception as ex:
        print("error: " + str(ex))
        sys.exit(-1)


if __name__ == "__main__":
    _main()
