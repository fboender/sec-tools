import sys
import argparse
import os
import logging
import json

import binlink
import common
import morestd
import tools


def verify_root():
    """
    Verify the user is root.
    """
    if os.getuid() != 0:
        sys.stderr.write("iptables viewing requires you be root.\n")
        sys.exit(2)


def gather():
    output = morestd.shell.cmd('iptables-save')['stdout']
    return common.IptablesParser(output).parse()

@binlink.register("sec-gather-iptables")
def cmdline(version):
    parser = argparse.ArgumentParser(description='Gather iptables firewall status')
    common.arg_add_defaults(parser, version=version)
    args = parser.parse_args()
    common.configure_logger(args.debug)

    verify_root()

    results = gather()

    sys.stdout.write(json.dumps({"iptables": results}, indent=4))
