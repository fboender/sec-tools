import argparse
import sys

import binlink
import common


@binlink.register("sec-tool")
def cmdline(version):
    parser = argparse.ArgumentParser(
        description='Wrapper executable for sec-tools. Don\'t call directly'
    )
    common.arg_add_defaults(parser, version=version)
    args = parser.parse_args()

    sys.stdout.write("This is a wrapper executable for sec-tools. "
                     "The following modules are available:\n\n")
    for bin in binlink.binlinks.keys():
        sys.stdout.write("  {}\n".format(bin))

    sys.stdout.write("\nYou can call them from the commandline. E.g:\n\n"
                     "  $ sec-gather-unixusers\n\n"
                     "More info on each module can be found in their man "
                     "pages:\n\n"
                     "  $ man sec-gather-unixusers\n\n")
